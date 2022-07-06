from authlib.integrations.flask_client import OAuth
import time
import logging
import json
from functools import wraps
from flask import request, session, redirect, url_for, g, current_app, abort

__all__ = ["OpenIDConnect"]

logger = logging.getLogger(__name__)


def _json_loads(content):
    if not isinstance(content, str):
        content = content.decode("utf-8")
    return json.loads(content)


class OpenIDConnect:
    def __init__(
        self, app=None, credentials_store=None, http=None, time=None, urandom=None
    ):
        secrets = self.load_secrets(app)
        self.client_secrets = list(secrets.values())[0]

        self.oauth = OAuth(app)

# TODO need to think a little abou tthis oidc realm config

        app.config.setdefault("OIDC_OPENID_REALM", "/oidc_callback")
        app.config.setdefault("OIDC_CLIENT_ID", self.client_secrets["client_id"])
        app.config.setdefault(
            "OIDC_SERVER_METADATA_URL",
            f"{self.client_secrets['issuer']}/.well-known/openid-configuration",
        )

# TODO build the userinfo uri from the issuer uri

        app.config.setdefault("OIDC_USERINFO_URL", self.client_secrets["userinfo_uri"])
        app.config.setdefault(
            "OIDC_CLIENT_SECRET", self.client_secrets.get("client_secret")
        )
        if self.client_secrets.get("scopes"):
            app.config.setdefault("OIDC_SCOPES", self.client_secrets.get("scopes"))
        else:
            app.config.setdefault("OIDC_SCOPES", "openid profile email")

        app.config.setdefault("OIDC_CLIENT_AUTH_METHOD", "client_secret_post")
        self.oauth.register(
            name="oidc",
            server_metadata_url=app.config["OIDC_SERVER_METADATA_URL"],
            client_kwargs={
                "scope": " ".join(app.config["OIDC_SCOPES"]),
                "token_endpoint_auth_method": app.config["OIDC_CLIENT_AUTH_METHOD"],
            },
        )
        app.route(app.config["OIDC_OPENID_REALM"])(self._oidc_callback)
        app.before_request(self._before_request)
        app.after_request(self._after_request)

    def _before_request(self):
        self.check_token_expiry()

    def _after_request(self, response):
        return response

    def _oidc_callback(self):
        try:
            session["token"] = self.oauth.oidc.authorize_access_token()
        except AttributeError:
            raise
        return redirect("/")

    def check_token_expiry(self):
        try:
            token = session.get("token")
            if token:
                if session.get("token")["expires_at"] - 60 < int(time.time()):
                    self.logout()
        except Exception:
            session.pop("token", None)
            session.pop("userinfo", None)
            raise

    @property
    def user_loggedin(self):
        """
        Represents whether the user is currently logged in.

        Returns:
            bool: Whether the user is logged in with Flask-OIDC.

        .. versionadded:: 1.0
        """
        return session.get("token") is not None

    def _retrieve_userinfo(self, access_token=None):
        """
        Requests extra user information from the Provider's UserInfo and
        returns the result.

        :returns: The contents of the UserInfo endpoint.
        :rtype: dict
        """
        if "userinfo_uri" not in self.client_secrets:
            logger.debug("Userinfo uri not specified")
            raise AssertionError("UserInfo URI not specified")

        # Cache the info from this request
        token = session.get("token")
        userinfo = session.get("userinfo")
        if userinfo:
            return userinfo
        else:
            try:
                resp = self.oauth.oidc.get(
                    current_app.config["OIDC_USERINFO_URL"], token=token
                )
                userinfo = resp.json()
                session["userinfo"] = userinfo
                return userinfo
            except Exception:
                raise

    def require_login(self, view_func):
        """
        Use this to decorate view functions that require a user to be logged
        in. If the user is not already logged in, they will be sent to the
        Provider to log in, after which they will be returned.

        .. versionadded:: 1.0
           This was :func:`check` before.
        """

        @wraps(view_func)
        def decorated(*args, **kwargs):
            if session.get("token") is None:
                redirect_uri = url_for(
                    "_oidc_callback", _scheme="https", _external=True
                )
                return self.oauth.oidc.authorize_redirect(redirect_uri)
            return view_func(*args, **kwargs)

        return decorated

    def logout(self):
        """
        Request the browser to please forget the cookie we set, to clear the
        current session.

        Note that as described in [1], this will not log out in the case of a
        browser that doesn't clear cookies when requested to, and the user
        could be automatically logged in when they hit any authenticated
        endpoint.

        [1]: https://github.com/puiterwijk/flask-oidc/issues/5#issuecomment-86187023

        .. versionadded:: 1.0
        """
        session.pop("token", None)
        session.pop("userinfo", None)
        return redirect("/")

    def load_secrets(self, app):
        # Load client_secrets.json to pre-initialize some configuration
        content = app.config["OIDC_CLIENT_SECRETS"]
        if isinstance(content, dict):
            return content
        else:
            return _json_loads(open(content, "r").read())

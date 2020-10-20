from pprint import pformat

import flask
from flask_openid import OpenID

app = flask.Flask(__name__)
app.config.from_object("test_auth.defaults")
app.config.from_envvar("TESTAUTH_SETTINGS")

oid = OpenID(app, "/var/tmp/openidstore", safe_roots=[])


@app.before_request
def before_request():
    flask.session.permanent = True


@app.route("/")
def home():
    user = pformat(flask.session.get("user"))
    user_info = pformat(flask.session.get("openid_response"))
    return flask.render_template("home.html", user=user, user_info=user_info)


@oid.after_login
def do_login(resp):
    flask.session["openid_response"] = resp
    user = {"openid_identity_url": resp.identity_url, "username": resp.nickname}
    flask.session["user"] = user
    app.logger.debug(f"{user}")
    return flask.redirect(flask.url_for(".home"))


@app.route("/login")
@oid.loginhandler
def login():
    if flask.session.get("user"):
        return flask.redirect(flask.url_for(".home"))
    return oid.try_login(
        app.config["OPENID_ENDPOINT"],
        ask_for=app.config["OPENID_ASK_FOR"],
        ask_for_optional=app.config["OPENID_ASK_FOR_OPTIONAL"],
    )


@app.route("/logout")
def logout():
    flask.session.pop("user", None)
    flask.session.pop("openid_response", None)
    flask.flash("You have been logged out", "info")
    return flask.redirect(flask.url_for(".home"))

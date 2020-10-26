from pprint import pformat

import flask
from flask_openid import OpenID
from test_auth.utilities import create_flask_app

app = create_flask_app(__name__)

oid = OpenID(app, "/var/tmp/openidstore", safe_roots=[])


@app.before_request
def before_request():
    flask.session.permanent = True


@app.route("/")
def home():
    try:
        user_data = pformat(flask.g.openid_user)
    except AttributeError:
        user_data = None
    return flask.render_template("home.html", user_data=user_data)


@oid.after_login
def do_login(resp):
    user = {"openid_identity_url": resp.identity_url}
    for attr in app.config["OPENID_ASK_FOR"] + app.config["OPENID_ASK_FOR_OPTIONAL"]:
        user[attr] = getattr(resp, attr)
    user["extensions"] = resp.extensions
    flask.g.openid_user = user
    return flask.redirect(flask.url_for(".home"))


@app.route("/login")
@oid.loginhandler
def login():
    if getattr(flask.g, "openid_user", None):
        return flask.redirect(flask.url_for(".home"))
    return oid.try_login(
        app.config["OPENID_ENDPOINT"],
        ask_for=app.config["OPENID_ASK_FOR"],
        ask_for_optional=app.config["OPENID_ASK_FOR_OPTIONAL"],
    )


@app.route("/logout")
def logout():
    flask.g.openid_user = None
    flask.flash("You have been logged out", "info")
    return flask.redirect(flask.url_for(".home"))

from pprint import pformat

import flask
from flask_oidc import OpenIDConnect

# Set up Flask application
app = flask.Flask(__name__)

app.config.from_object("test_auth.defaults")
app.config.from_envvar("TESTAUTH_SETTINGS")


# Set up FAS extension
OIDC = OpenIDConnect(app, credentials_store=flask.session)


@app.before_request
def before_request():
    """Set the flask session as permanent."""
    flask.session.permanent = True


@app.route("/")
def home():
    user_info = OIDC._retrieve_userinfo()
    return flask.render_template("home.html", OIDC=OIDC, user_info=pformat(user_info))


@app.route("/login")
@OIDC.require_login
def login():
    return flask.redirect(flask.url_for(".home"))


@app.route("/logout")
def logout():
    if OIDC.user_loggedin:
        OIDC.logout()
        flask.flash("You have been logged out")
    return flask.redirect(flask.url_for(".home"))

from pprint import pformat

import flask
from flask_oidc import OpenIDConnect
from test_auth.utilities import create_flask_app

# Set up Flask application
app = create_flask_app(__name__)

# Set up FAS extension
OIDC = OpenIDConnect(app, credentials_store=flask.session)


@app.before_request
def before_request():
    """Set the flask session as permanent."""
    flask.session.permanent = True


@app.route("/")
def home():
    if OIDC.user_loggedin:
        user_data = pformat(OIDC._retrieve_userinfo())
    else:
        user_data = None
    return flask.render_template("home.html", user_data=user_data)


@app.route("/login")
@OIDC.require_login
def login():
    return flask.redirect(flask.url_for(".home"))


@app.route("/logout")
def logout():
    if OIDC.user_loggedin:
        OIDC.logout()
        flask.flash("You have been logged out", "info")
    return flask.redirect(flask.url_for(".home"))

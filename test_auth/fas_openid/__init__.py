from pprint import pformat

import flask
import flask_fas_openid
from test_auth.utilities import create_flask_app

app = create_flask_app(__name__)
FAS = flask_fas_openid.FAS(app)


@app.before_request
def before_request():
    flask.session.permanent = True


@app.route("/")
def home():
    user_data = pformat(flask.g.fas_user)
    return flask.render_template("home.html", user_data=user_data)


@FAS.postlogin
def do_login(return_url):
    return flask.redirect(flask.url_for(".home"))


@app.route("/login")
def login():
    if flask.g.fas_user:
        return flask.redirect(flask.url_for(".home"))
    return FAS.login(flask.url_for(".home"))


@app.route("/logout")
def logout():
    FAS.logout()
    flask.flash("You have been logged out", "info")
    return flask.redirect(flask.url_for(".home"))

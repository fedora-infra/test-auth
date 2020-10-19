from flask import Flask, render_template, abort, session, url_for
from flask_oidc import OpenIDConnect

# Set up Flask application
app = Flask(__name__)

app.config.from_object('test_auth.defaults')
app.config.from_envvar('TESTAUTH_SETTINGS')


# Set up FAS extension
OIDC = OpenIDConnect(app, credentials_store=session)


@app.before_request
def before_request():
    """Set the flask session as permanent."""
    session.permanent = True

@app.route("/")
def home():
    return render_template("home.html", OIDC=OIDC)

@app.route("/login")
@OIDC.require_login
def login():
    return flask.redirect(flask.url_for('.home'))

@app.route("/logout")
def logout():
    if OIDC.user_loggedin:
        OIDC.logout()
        flask.flash('You have been logged out')
    return flask.redirect(flask.url_for('.home'))

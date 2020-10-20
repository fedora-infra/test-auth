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
    return flask.render_template("home.html",)


@oid.after_login
def do_login(resp):
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
        ask_for=["email", "nickname", "fullname"],
        ask_for_optional=["language", "timezone"],
    )

@app.route("/logout")
def logout():
    flask.session["user"] = None
    flask.flash("You have been logged out", "info")
    return flask.redirect(flask.url_for(".home"))

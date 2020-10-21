import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix

from .fas_openid import app as fas_openid_app
from .oidc import app as oidc_app
from .openid import app as openid_app

root_app = flask.Flask(__name__)


@root_app.route("/")
def root():
    return flask.render_template("root.html")


application = DispatcherMiddleware(
    root_app, {"/oidc": oidc_app, "/openid": openid_app, "/fas-openid": fas_openid_app}
)

application = ProxyFix(application, x_proto=1, x_host=1)

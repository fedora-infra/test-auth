from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix
from .oidc import app as oidc_app
from .openid import app as openid_app

root_app = flask.Flask(__name__)

@root_app.route("/")
def root():
    return flask.Response("""
<html>
<body>
    <p>Login with:</p>
    <ul>
        <li><a href="oidc/">OpenID Connect (OIDC)</a></li>
        <li><a href="openid/">OpenID</a></li>
    </ul>
</body>
</html>
""")


application = DispatcherMiddleware(root_app, {
    "/oidc": oidc_app,
    '/openid': openid_app
})

application.wsgi_app = ProxyFix(application.wsgi_app, x_proto=1, x_host=1)

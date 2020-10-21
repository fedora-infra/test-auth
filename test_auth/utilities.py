import os

from flask import Flask


def create_flask_app(*args, **kwargs):
    app = Flask(*args, **kwargs)

    app.config.from_object("test_auth.defaults")
    if "TESTAUTH_SETTINGS" in os.environ:
        app.config.from_envvar("TESTAUTH_SETTINGS")

    app.jinja_loader.searchpath.append(os.path.join(app.root_path, "..", "templates"))

    return app

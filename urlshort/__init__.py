from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    #Allow to securely send messages to the user
    app.secret_key = 'hweiweninwisdsd'

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app
# initialize app

from flask import Flask


def create_app():
    # construct the core application
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RR'

    with app.app_context():
        # import main Blueprint
        from . import routes
        app.register_blueprint(routes.flaskaiapp)  # should flaskaiapp in routes file

        # import dash application
        from dashapp import dashfile
        app = dashfile.Add_Dash(app)

        return app

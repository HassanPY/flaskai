from flask import Flask


def create_app():
    # Construct the core application.
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    with app.app_context():

        # Import main Blueprint
        from generalapp.generalfile import general_bp
        app.register_blueprint(general_bp, url_prefix='/site')

        # Import Dash application
        from dashapp.dashfile import Add_Dash

        app = Add_Dash(app)

        return app

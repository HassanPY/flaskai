# Usually we amke the Blueprint registartion in wsgi.py
# but to get Dash works with Flask we have to make a work arround,
# as part of this work arround we make the registration in __init__

from __init__ import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


# from flask import Flask
#
# # Blueprint Registration
#
# from generalapp.generalfile import general_bp
# from dashapp.dashfile import dash_bp
#
# flask_app = Flask(__name__)
#
# flask_app.register_blueprint(general_bp, url_prefix='/site')
# flask_app.register_blueprint(dash_bp, url_prefix='/dash')
#
# if __name__ == "__main__":
#     flask_app.run(host='0.0.0.0', debug=True)

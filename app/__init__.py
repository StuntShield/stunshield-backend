from flask import Flask
from .routes.blueprint import blueprint
from .handlers.ErrorHandlers import ErrorHandlers
from .config import main_config as config


def create_app():
    app = Flask(__name__)  # flask app object
    # app.config.from_object("config")  # Configuring from Python Files

    return app


app = create_app()  # Creating the app
# Registering the blueprint
app.register_blueprint(blueprint, url_prefix='/')

# handling errors
http_codes = [404, 500, 405]

for c in http_codes:
    app.register_error_handler(c, ErrorHandlers.common)


if __name__ == '__main__':  # Running the app
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
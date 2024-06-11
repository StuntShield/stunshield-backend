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
app.register_error_handler(404, ErrorHandlers.page_not_found)
app.register_error_handler(500, ErrorHandlers.internal_server_error)

if __name__ == '__main__':  # Running the app
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

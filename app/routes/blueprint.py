from flask import Blueprint

from .controllers.LLMController import getPrompt
from .controllers.ArticleController import getArticles

from .controllers.StuntingController import StuntingController

blueprint = Blueprint('blueprint', __name__)


# define the routes
blueprint.route('/', methods=['GET'])(StuntingController.index)
blueprint.route('/articles', methods=['GET'])(getArticles)
blueprint.route('/prompt', methods=['GET'])(getPrompt)
blueprint.route('/stunting-classification', methods=['POST'])(
    StuntingController.predict_stunting
)
# blueprint.route("/create", methods=["GET"])(create)
# blueprint.route("/insert", methods=["GET"])(insert)
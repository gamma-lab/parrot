from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def index():
    return 'api is available', 200


from . import users
from . import domains
from . import actions
from . import stories
from . import intents
from . import story_lines
from . import user_says_examples

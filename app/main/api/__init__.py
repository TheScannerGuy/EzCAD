from flask_restx import Api
from flask import Blueprint

from .user import api as user
from .character import api as character
from .vehicle import api as vehicle
from .server import api as server
from .unit import api as unit
from .call import api as call
from .department import api as department

api_blueprint = Blueprint('api', __name__)

api = Api(api_blueprint)

api.add_namespace(user, path='/user')
api.add_namespace(character, path='/character')
api.add_namespace(vehicle, path='/vehicle')
api.add_namespace(server, path='/server')
api.add_namespace(unit, path='/unit')
api.add_namespace(call, path='/call')
api.add_namespace(department, path='/department')


def requires_perm(perm):
    def inner():
        return True

    return inner

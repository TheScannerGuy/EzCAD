from flask_restx import Namespace, Resource, reqparse
from ... import discord
from ..interfaces import (
    units,
    register_unit
)
from ..models import *
from ..schemas import UnitSchema
from werkzeug.exceptions import (
    NotFound,
    BadRequest,
    Conflict
)

api = Namespace('unit')


@api.route('/register')
@api.doc(params={"unitId": "Unit ID", "departmentId": "Department ID"})
class RegisterUnit(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('unitId', type=str)
        parser.add_argument('departmentId', type=int)
        args = parser.parse_args()
        register_unit(args["unitId"], args["departmentId"])
        return CurrentUnit().get()


@api.route('/current')
@api.response(404, 'Unit is not registered')
class CurrentUnit(Resource):
    def get(self):
        user = discord.fetch_user()
        if any(unit.discord_id == user.id for unit in units):
            for unit in units:
                if unit.discord_id == user.id:
                    return UnitSchema().dump(unit)
        raise NotFound


@api.route('/current/status/<int:statusId>')
@api.response(404, 'Unit is not registered')
@api.response(200, 'Status changed')
class CurrentUnitStatus(Resource):
    def post(self, statusId: int):
        user = discord.fetch_user()
        if any(unit.discord_id == user.id for unit in units):
            if any(unit.discord_id == user.id for unit in units):
                for unit in units:
                    if unit.discord_id == user.id:
                        unit.status = statusId
                        return UnitSchema().dump(unit), 200
        raise NotFound


@api.route('/all')
class AllUnits(Resource):
    def get(self):
        return UnitSchema(many=True).dump(units)



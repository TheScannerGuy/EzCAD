from flask_restx import Namespace, Resource, reqparse
from ... import discord
from ..interfaces import (
    units,
    register_unit,
    calls
)
from ..models import *
from ..schemas import UnitSchema
from werkzeug.exceptions import *

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


@api.route('/status/<int:statusId>')
@api.response(404, 'Unit is not registered')
@api.response(400, 'Invalid status')
@api.response(200, 'Status changed')
class ChangeUnitStatus(Resource):
    def post(self, statusId: int):
        parser = reqparse.RequestParser()
        parser.add_argument('unitId', type=str)
        args = parser.parse_args()

        unit = next((i for i in units if i.unit_id == args["unitId"]), None)
        if unit is None:
            raise NotFound
        if statusId < 0 or statusId > 7:
            raise BadRequest

        unit.status = statusId

        return UnitSchema().dump(unit)


@api.route('/attach')
@api.response(404, 'Unit is not registered')
@api.response(200, 'Attached to assignment')
class AttachUnit(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('unitId', type=str)
        parser.add_argument('callId', type=str)
        args = parser.parse_args()

        unit = next((i for i in units if i.unit_id == args["unitId"]), None)
        call = next((i for i in calls if i.callId == args["callId"]), None)

        if (call is None) or (unit is None):
            raise NotFound

        unit.currentCall = call
        unit.status = 4

        return UnitSchema().dump(unit)


@api.route('/all')
class AllUnits(Resource):
    def get(self):
        return UnitSchema(many=True).dump(units)



from flask_restx import Namespace, Resource, reqparse
from ... import discord
from ..schemas import *
from ..models import *
from ..interfaces import Call, create_call, calls, units
from werkzeug.exceptions import *

api = Namespace('call')


@api.route('/create')
class CreateCall(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=int)
        parser.add_argument('subTypeCode', type=str)
        parser.add_argument('postal', type=int)
        parser.add_argument('location', type=str)
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        call = create_call(args["type"], args["subTypeCode"], args["postal"],
                           args["location"], args["description"])

        return CallSchema().dump(call)


@api.route('/delete/<string:call_id>')
@api.response(404, 'Call does not exist')
class DeleteCall(Resource):
    def delete(self, call_id):
        call = next((i for i in calls if i.callId == call_id), None)
        if call is None:
            raise NotFound

        calls.pop(call)
        del call


@api.route('/types')
class CallTypes(Resource):
    def get(self):
        call_types = CallTypeModel.query.all()
        return CallTypeSchema(many=True).dump(call_types)


@api.route('/current')
@api.response(404, 'Unit or call not found')
class CurrentCall(Resource):
    def get(self):
        user = discord.fetch_user()
        if any(unit.discord_id == user.id for unit in units):
            for unit in units:
                if (unit.discord_id == user.id) and (unit.currentCall is not None):
                    return CallSchema().dump(unit.currentCall)
        raise NotFound


@api.route('/all')
class AllCalls(Resource):
    def get(self):
        return CallSchema(many=True).dump(calls)


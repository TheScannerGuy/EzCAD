from flask_restx import Namespace, Resource, reqparse, fields
from flask import request
from ..models import VehicleModel
from ..schemas import VehicleSchema

api = Namespace('vehicle')

vehicle_model = api.model('VehicleModel', {
    'licensePlate': fields.String,
    'characterId': fields.Integer,
    'stolen': fields.Integer
})


@api.route('/create')
@api.param('licensePlate', 'License Plate')
@api.param('characterId', 'Character ID', type=int)
@api.param('stolen', 'Stolen?', type=int)
class CreateVehicle(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('licensePlate', type=str)
        parser.add_argument('characterId', type=int)
        parser.add_argument('stolen', type=int)
        args = parser.parse_args()

        VehicleModel.create(
            license_plate=args["licensePlate"].upper(),
            character_id=args["characterId"],
            stolen=args["stolen"]
        )


@api.route('/<string:licensePlate>')
@api.param('licensePlate', 'License Plate')
@api.response(404, 'Vehicle does not exist')
class VehicleResource(Resource):
    def get(self, licensePlate):
        vehicle = VehicleModel.query.filter_by(license_plate=licensePlate).first()
        if vehicle is None:
            return 404
        return VehicleSchema().dump(vehicle)

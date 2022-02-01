from flask_restx import Namespace, Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from ... import allowed_file, UPLOAD_FOLDER
import os
from ..models import (
    TenCodeModel,
    CallTypeModel,
    OffenseModel
)
from ..schemas import (
    TenCodeSchema,
    CallSchema,
    ChargeSchema
)

api = Namespace('server')


@api.route('/discord/guild/<int:guildId>')
class DiscordGuild(Resource):
    def post(self, guildId):
        return

@api.route('/tencodes')
class TenCodes(Resource):
    def get(self):
        tencodes = TenCodeModel.query.all()
        return TenCodeSchema(many=True).dump(tencodes)


@api.route('/penalcode')
class PenalCode(Resource):
    def get(self):
        charges = OffenseModel.query.all()
        return ChargeSchema(many=True).dump(charges)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        parser.add_argument('type')
        parser.add_argument('description')
        parser.add_argument('fine')
        args = parser.parse_args()

        OffenseModel.create(code=args["code"], type=args["type"],
                            description=args["description"], fine=args["fine"])

        return 200


upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@api.route('/penalcode/upload')
@api.expect(upload_parser)
class UploadPenalCode(Resource):
    def post(self):
        args = upload_parser.parse_args()
        file = args['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            OffenseModel.add_upload(os.path.join(UPLOAD_FOLDER, filename))
            return 200


@api.route('/calls')
class Calls(Resource):
    def get(self):
        call_types = CallTypeModel.query.all()
        return CallSchema(many=True).dump(call_types)

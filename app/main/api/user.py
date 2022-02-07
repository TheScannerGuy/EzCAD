from flask_restx import Namespace, Resource, reqparse
from flask_discord import Unauthorized
from ... import discord
from ..models import *
from ..schemas import *
from werkzeug.exceptions import *

api = Namespace('user')


@api.route('/register')
@api.param('username', 'Discord Username')
@api.param('discriminator', 'Discord Discriminator')
@api.param('discordId', 'Discord ID')
class CreateUser(Resource):
    """
    Resource is for testing only. Remove for deployment.
    """
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('discriminator', type=int)
        parser.add_argument('discordId', type=str)
        args = parser.parse_args()

        user = UserModel.query.fitler_by(discord_id=args["discordId"]).first()
        if user is not None:
            return "User already exists", 409

        UserModel.register(discord_id=args["discordId"], username=args["username"],
                           discriminator=args["discriminator"], avatar=args["avatar"],
                           banned=0, admin=0)
        return 200


@api.route('/all')
class AllUsers(Resource):
    def get(self):
        all_users = UserModel.query.all()
        return UserSchema(many=True).dump(all_users)


@api.route('/<int:discordId>')
@api.param('discordId', 'Discord ID')
@api.response(404, 'User does not exist')
class UserById(Resource):
    def get(self, discordId):
        user = UserModel.query.filter_by(discord_id=discordId).first()
        if user is None:
            return 404
        else:
            for character in user.characters:
                print(character.first_name)
            return UserSchema().dump(user)


@api.route('/current')
@api.response(404, 'User does not exist')
class CurrentUser(Resource):
    def get(self):
        try:
            user = UserModel.query.filter_by(discord_id=discord.fetch_user().id).first()
        except Exception as e:
            raise NotFound
        if user is None:
            raise NotFound
        return UserSchema().dump(user)


@api.route('/<int:discordId>/delete')
@api.response(404, 'User does not exist')
class DeleteUser(Resource):
    def delete(self, discordId):
        user = UserModel.query.filter_by(discord_id=discordId).first()

        if user is None:
            return 404

        return 200


@api.route('/<int:discordId>/department/<int:departmentId>')
@api.response(404, 'User does not exist')
@api.response(400, 'Department ID does not exist')
@api.response(409, 'Already exists as requested. Nothing to change.')
@api.response(200, 'Amended Department to User')
class UserDepartment(Resource):
    def validate(self, discordId, departmentId):
        dept = DepartmentModel.query.filter_by(id=departmentId).first()
        user = UserModel.query.filter_by(discord_id=discordId).first()
        if dept is None:
            raise BadRequest
        if user is None:
            raise NotFound

        return True

    def put(self, discordId, departmentId):
        if self.validate(discordId, departmentId):
            x = UserDepartmentModel.query.filter_by(discord_id=discordId, dept_id=departmentId).first()
            if x is not None:
                raise Conflict
            else:
                UserDepartmentModel.create(discord_id=discordId, dept_id=departmentId)
                return UserById().get(discordId)

    def delete(self, discordId, departmentId):
        if self.validate(discordId, departmentId):
            x = UserDepartmentModel.query.filter_by(discordId=discordId, departmentId=departmentId).first()
            if x is None:
                raise Conflict
            else:
                UserDepartmentModel.delete(x)
                return UserById().get(discordId)

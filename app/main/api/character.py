from flask_restx import Namespace, Resource, reqparse
from ... import discord
from flask import request
from random import randint
from ..models import *
from werkzeug.exceptions import *
from ..schemas import CharacterSchema
from ..interfaces import random_id

api = Namespace('character')


@api.route('/create')
@api.param('firstName', 'First Name')
@api.param('lastName', 'Last Name')
@api.param('address', 'Address')
@api.param('dateOfBirth', 'Date of Birth')
@api.param('sex', 'Sex/Gender')
@api.param('race', 'Race')
@api.param('eyes', 'Eye color')
@api.param('height', 'Height (ft-in)')
class CreateCharacter(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstName', type=str)
        parser.add_argument('lastName', type=str)
        parser.add_argument('address', type=str)
        parser.add_argument('dateOfBirth', type=str)
        parser.add_argument('sex', type=str)
        parser.add_argument('race', type=str)
        parser.add_argument('eyes', type=str)
        parser.add_argument('height', type=str)
        args = parser.parse_args()

        character_id = random_id()

        CharacterModel.create(
            character_id=character_id,
            discord_id=discord.fetch_user().id,
            first_name=args["firstName"].upper(),
            last_name=args["lastName"].upper(),
            address=args["address"],
            date_of_birth=args["dateOfBirth"],
            sex=args["sex"],
            race=args["race"],
            eyes=args["eyes"],
            height=args["height"]
        )

        return CharacterSchema().dump(CharacterModel.query.filter_by(character_id=character_id).first())


@api.route('/search')
@api.param('firstName', 'First Name')
@api.param('lastName', 'Last Name')
@api.response(404, 'Character does not exist')
class CharacterSearch(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstName', type=str)
        parser.add_argument('lastName', type=str)
        args = parser.parse_args()

        characters = CharacterModel.query.filter_by(first_name=args["firstName"].upper(),
                                                    last_name=args["lastName"].upper()).all()

        return CharacterSchema(many=True).dump(characters)


@api.route('/<int:characterId>')
@api.response(404, 'Character does not exist')
class CharacterById(Resource):
    def get(self, characterId):
        character = CharacterModel.query.filter_by(character_id=characterId).first()
        if character is None:
            raise NotFound

        return CharacterSchema().dump(character)


@api.route('/<int:characterId>/license/<int:licenseId>/<int:value>')
@api.response(404, 'Character/License does not exist')
class LicenseCharacter(Resource):
    def post(self, characterId, licenseId, value):
        character = CharacterModel.query.filter_by(character_id=characterId).first()
        _license = LicenseModel.query.filter_by(
            license_id=licenseId).first()  # Use _license as license shadows builtin function
        if (character is None) or (_license is None):
            raise NotFound

        CharacterLicenseModel.create(character_id=characterId, license_id=licenseId, value=value)
        return CharacterSchema().dump(character)


@api.route('/<int:characterId>/citation')
@api.response(404, 'Character does not exist')
@api.doc(params={'charges': 'List of charge codes', 'location': 'Location', 'notes': 'Notes'})
class CiteCharacter(Resource):
    def put(self, characterId):
        parser = reqparse.RequestParser()
        parser.add_argument('charges', required=True)  # List of charges
        parser.add_argument('location', type=str)
        parser.add_argument('notes', type=str)
        args = parser.parse_args()

        character = CharacterModel.query.filter_by(character_id=characterId).first()
        if character is None:
            raise NotFound

        citation_id = random_id()

        CitationModel.create(citation_id=citation_id, character_id=characterId,
                             officer_id=discord.fetch_user().id, location=args['location'], notes=args['notes'])

        charges = args["charges"].split()  # Convert to list
        for i in charges:
            CitationChargeModel.create(citation_id=citation_id, charge_code=i)

        return CharacterSchema().dump(character)


@api.route('/<int:characterId>/warning')
@api.response(404, 'Character does not exist')
@api.doc(params={'charges': 'List of charge codes', 'location': 'Location', 'notes': 'Notes'})
class CiteCharacter(Resource):
    def put(self, characterId):
        parser = reqparse.RequestParser()
        parser.add_argument('charges', required=True)  # List of charges
        parser.add_argument('location', type=str)
        parser.add_argument('notes', type=str)
        args = parser.parse_args()

        character = CharacterModel.query.filter_by(character_id=characterId).first()
        if character is None:
            raise NotFound

        warning_id = random_id()

        WarningModel.create(warning_id=warning_id, character_id=characterId,
                            officer_id=discord.fetch_user().id, location=args['location'], notes=args['notes'])

        charges = args["charges"].split()  # Convert to list
        for i in charges:
            WarningChargeModel.create(warning_id=warning_id, charge_code=i)

        return CharacterSchema().dump(character)


@api.route('/<int:characterId>/arrest')
@api.response(404, 'Character does not exist')
@api.doc(params={'charges': 'List of charge codes', 'location': 'Location', 'notes': 'Notes'})
class CiteCharacter(Resource):
    def put(self, characterId):
        parser = reqparse.RequestParser()
        parser.add_argument('charges', required=True)  # List of charges
        parser.add_argument('location', type=str)
        parser.add_argument('notes', type=str)
        args = parser.parse_args()

        character = CharacterModel.query.filter_by(character_id=characterId).first()
        if character is None:
            raise NotFound

        arrest_id = random_id()

        ArrestModel.create(arrest_id=arrest_id, character_id=characterId,
                           officer_id=discord.fetch_user().id, location=args['location'], notes=args['notes'])

        charges = args["charges"].split()  # Convert to list
        for i in charges:
            ArrestChargeModel.create(arrest_id=arrest_id, charge_code=i)

        return CharacterSchema().dump(character)


@api.route('/all')
class AllCharacters(Resource):
    def get(self):
        all_characters = CharacterModel.query.all()
        return CharacterSchema(many=True).dump(all_characters)

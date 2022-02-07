from .. import db
from flask_discord.models import user as flask_discord_user
import json
from datetime import datetime
from random import randint


class BaseMixin(object):
    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()


class TimestampMixin(object):
    _t = datetime.utcnow().strftime('%b %d, %Y')

    created = db.Column(db.String(20), nullable=False, default=_t)
    updated = db.Column(db.String(20), onupdate=_t)


class ServerDataModel(db.Model):
    __tablename__ = "server"

    guild_id = db.Column(db.String(20), primary_key=True)


class DepartmentModel(db.Model, BaseMixin):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    type = db.Column(db.Integer)  # {0: Police, 1: 'Fire/EMS', 2: 'Dispatch', 3: 'Civilian', 4: 'Fire', 5: 'EMS'}

    users = db.relationship('UserDepartmentModel', back_populates='department')


class UserModel(db.Model):
    __tablename__ = "user"

    discord_id = db.Column(db.String(30), primary_key=True)
    username = db.Column(db.String(30))
    discriminator = db.Column(db.Integer)
    avatar = db.Column(db.String(35))
    suspended = db.Column(db.Integer)
    admin = db.Column(db.Integer)

    departments = db.relationship('UserDepartmentModel', back_populates='user')
    characters = db.relationship('CharacterModel', back_populates='user')

    @classmethod
    def register(cls, user: flask_discord_user, admin=0):
        """ Add User to database. Should be called when during flask_discord callback if user is not in db """

        u = cls(discord_id=user.id, username=user.username, discriminator=user.discriminator,
                avatar=user.avatar_hash, suspended=0, admin=admin)
        db.session.add(u)
        db.session.commit()

        return u


class UserDepartmentModel(db.Model, BaseMixin):
    __tablename__ = "userdepartment"

    discord_id = db.Column(db.String(30), db.ForeignKey('user.discord_id'))
    dept_id = db.Column(db.Integer, db.ForeignKey('department.id'), primary_key=True)
    callsign = db.Column(db.String, nullable=True)  # Default Callsign for Department

    user = db.relationship('UserModel', back_populates='departments')
    department = db.relationship('DepartmentModel', back_populates='users')


class CharacterModel(db.Model, BaseMixin):
    __tablename__ = "character"

    character_id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.Integer, db.ForeignKey('user.discord_id'))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    address = db.Column(db.String(40))
    date_of_birth = db.Column(db.String(20))
    sex = db.Column(db.String(1))
    race = db.Column(db.String(10))
    eyes = db.Column(db.String(3))
    height = db.Column(db.String(10))

    user = db.relationship('UserModel', back_populates='characters')
    licenses = db.relationship('CharacterLicenseModel', back_populates='character')
    vehicles = db.relationship('VehicleModel', back_populates='character')

    warnings = db.relationship('WarningModel', back_populates='character')
    citations = db.relationship('CitationModel', back_populates='character')
    arrests = db.relationship('ArrestModel', back_populates='character')


class VehicleModel(db.Model, BaseMixin):
    __tablename__ = "vehicle"

    license_plate = db.Column(db.String(10), primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.character_id'))
    stolen = db.Column(db.Integer)

    character = db.relationship('CharacterModel', back_populates='vehicles')
    warnings = db.relationship('WarningModel', back_populates='vehicle')
    citations = db.relationship('CitationModel', back_populates='vehicle')
    arrests = db.relationship('ArrestModel', back_populates='vehicle')


class WarningModel(db.Model, BaseMixin, TimestampMixin):
    __tablename__ = "warning"

    warning_id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.character_id'))
    officer_id = db.Column(db.Integer)  # Discord ID of reporting officer
    location = db.Column(db.String(30))
    notes = db.Column(db.String(240), nullable=True)
    license_plate = db.Column(db.String(10), db.ForeignKey('vehicle.license_plate'), nullable=True)

    charges = db.relationship('WarningChargeModel', back_populates='warning')
    character = db.relationship('CharacterModel', back_populates='warnings')
    vehicle = db.relationship('VehicleModel', back_populates='warnings')


class WarningChargeModel(db.Model, BaseMixin):
    __tablename__ = "warningcharge"

    id = db.Column(db.Integer, default=randint(10 ** (8 - 1), (10 ** 8) - 1), primary_key=True)
    warning_id = db.Column(db.Integer, db.ForeignKey('warning.warning_id'), )
    charge_code = db.Column(db.String(10), db.ForeignKey('offense.code'))

    warning = db.relationship('WarningModel', back_populates='charges')
    offense = db.relationship('OffenseModel', back_populates='warnings')


class CitationModel(db.Model, BaseMixin, TimestampMixin):
    __tablename__ = "citation"

    citation_id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.character_id'))
    officer_id = db.Column(db.Integer, db.ForeignKey('user.discord_id'))  # Discord ID of reporting officer
    location = db.Column(db.String(30))
    notes = db.Column(db.String(240), nullable=True)
    license_plate = db.Column(db.String(10), db.ForeignKey('vehicle.license_plate'), nullable=True)

    charges = db.relationship('CitationChargeModel', back_populates='citation', uselist=True)
    character = db.relationship('CharacterModel', back_populates='citations')
    vehicle = db.relationship('VehicleModel', back_populates='citations')


class CitationChargeModel(db.Model, BaseMixin):
    __tablename__ = "citationcharge"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    citation_id = db.Column(db.Integer, db.ForeignKey('citation.citation_id'))
    charge_code = db.Column(db.String(10), db.ForeignKey('offense.code'))

    citation = db.relationship('CitationModel', back_populates='charges')
    offense = db.relationship('OffenseModel', back_populates='citations')


class ArrestModel(db.Model, BaseMixin, TimestampMixin):
    __tablename__ = "arrest"

    arrest_id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.character_id'))
    officer_id = db.Column(db.Integer)  # Discord ID of reporting officer
    location = db.Column(db.String(30))
    notes = db.Column(db.String(240), nullable=True)
    license_plate = db.Column(db.String(10), db.ForeignKey('vehicle.license_plate'), nullable=True)

    charges = db.relationship('ArrestChargeModel', back_populates='arrest')
    character = db.relationship('CharacterModel', back_populates='arrests')
    vehicle = db.relationship('VehicleModel', back_populates='arrests')


class ArrestChargeModel(db.Model, BaseMixin):
    __tablename__ = "arrestcharge"
    id = db.Column(db.Integer, default=randint(10 ** (8 - 1), (10 ** 8) - 1), primary_key=True)
    arrest_id = db.Column(db.Integer, db.ForeignKey('arrest.arrest_id'), primary_key=True)
    charge_code = db.Column(db.String(10), db.ForeignKey('offense.code'))

    arrest = db.relationship('ArrestModel', back_populates='charges')
    offense = db.relationship('OffenseModel', back_populates='arrests')


class LicenseModel(db.Model, BaseMixin):
    __tablename__ = "license"

    license_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    characters = db.relationship('CharacterLicenseModel', back_populates='license')


class CharacterLicenseModel(db.Model, BaseMixin):
    __tablename__ = "characterlicense"

    character_id = db.Column(db.Integer, db.ForeignKey('character.character_id'))
    license_id = db.Column(db.Integer, db.ForeignKey('license.license_id'), nullable=False, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    character = db.relationship('CharacterModel', back_populates='licenses')
    license = db.relationship('LicenseModel', back_populates='characters')


class TenCodeModel(db.Model, BaseMixin):
    __tablename__ = "tencode"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    description = db.Column(db.String(30))


class OffenseModel(db.Model, BaseMixin):
    __tablename__ = "offense"

    code = db.Column(db.String(10), primary_key=True)
    type = db.Column(db.String(20))
    description = db.Column(db.String(30))
    fine = db.Column(db.Integer, nullable=True)

    citations = db.relationship('CitationChargeModel', back_populates='offense')
    warnings = db.relationship('WarningChargeModel', back_populates='offense')
    arrests = db.relationship('ArrestChargeModel', back_populates='offense')

    @classmethod
    def add_upload(cls, file_path):
        """ Add uploaded json file """
        f = open(file_path)
        data = json.load(f)
        f.close()

        for charge in data:
            c = cls(code=charge["code"], type=charge["type"], description=charge["description"],
                    fine=charge["fine"])
            db.session.add(c)
        db.session.commit()


class CallTypeModel(db.Model, BaseMixin):
    __tablename__ = "calltype"

    type = db.Column(db.String(50))
    code = db.Column(db.String(10), primary_key=True)

from .. import ma
from .models import *


class UnitSchema(ma.Schema):
    class Meta:
        fields = ("unit_id", "dept_id", "discord_id", "status", "currentCall")

    user = ma.Nested("UserSchema")


class CallSchema(ma.Schema):
    class Meta:
        fields = ("typeCode", "postal", "location", "description", "units")

    units = ma.Nested("UnitSchema", many=True)


class DepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DepartmentModel

    users = ma.Nested("UserDepartmentSchema", exclude=["department"], many=True)


class LicenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LicenseModel


class CharacterLicenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CharacterLicenseModel

    character = ma.Nested("CharacterSchema")
    license = ma.Nested("LicenseSchema")


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel

    departments = ma.Nested("UserDepartmentSchema", exclude=["user", "discord_id"], many=True)
    characters = ma.Nested("CharacterSchema", exclude=["user"], many=True)
    default_ids = ma.Nested("DefaultIdSchema", exclude=["user"])


class UserDepartmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDepartmentModel
        include_fk = True

    user = ma.Nested("UserSchema", exclude=["departments"])
    department = ma.Nested("DepartmentSchema", exclude=["users", 'id'])


class CharacterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CharacterModel

    user = ma.Nested(UserSchema, exclude=["characters"])
    vehicles = ma.Nested("VehicleSchema", exclude=['character', 'citations', 'arrests', 'warnings'], many=True)
    citations = ma.Nested("CitationSchema", many=True)
    arrests = ma.Nested("ArrestSchema", many=True)
    warnings = ma.Nested("WarningSchema", many=True)
    licenses = ma.Nested("CharacterLicenseSchema", exclude=["character"], many=True)


class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VehicleModel

    character = ma.Nested(CharacterSchema)
    citations = ma.Nested("CitationSchema", many=True)
    arrests = ma.Nested("ArrestSchema", many=True)
    warnings = ma.Nested("WarningSchema", many=True)


class _ChargeMixin(object):
    offense = ma.Nested('ChargeSchema')
    vehicle = ma.Nested('VehicleSchema')


class CitationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CitationModel

    charges = ma.Nested('CitationChargeSchema', exclude=['citation'], many=True)


class CitationChargeSchema(ma.SQLAlchemyAutoSchema, _ChargeMixin):
    class Meta:
        model = CitationChargeModel

    citation = ma.Nested('CitationSchema')


class WarningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WarningModel

    charges = ma.Nested('WarningChargeSchema', many=True)


class WarningChargeSchema(ma.SQLAlchemyAutoSchema, _ChargeMixin):
    class Meta:
        model = WarningChargeModel


class ArrestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ArrestModel

    charges = ma.Nested('ArrestChargeSchema', many=True)


class ArrestChargeSchema(ma.SQLAlchemyAutoSchema, _ChargeMixin):
    class Meta:
        model = ArrestChargeModel


class TenCodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TenCodeModel


class ChargeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OffenseModel


class CallTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CallTypeModel

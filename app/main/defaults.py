import json

from app.main.models import (
    CallTypeModel,
    DepartmentModel,
    LicenseModel,
    TenCodeModel,
    OffenseModel
)

defaults = {
    "app/db-defaults/call-types.json": CallTypeModel,
    "app/db-defaults/departments.json": DepartmentModel,
    "app/db-defaults/licenses.json": LicenseModel,
    "app/db-defaults/tencodes.json": TenCodeModel,
    "app/db-defaults/offenses.json": OffenseModel
}

primary_key = {
    CallTypeModel: 'code',
    DepartmentModel: 'id',
    LicenseModel: 'license_id',
    TenCodeModel: 'id',
    OffenseModel: 'code'
}


def init_defaults():
    print('Loading defaults')
    for i in defaults:
        model = defaults[i]
        pk = primary_key[model]
        f = open(i, 'r')
        data = json.load(f)
        f.close()

        for x in data:
            try:
                if model.query.filter_by(**{pk: x[pk]}).first() is not None:
                    continue
            except KeyError:
                print('ERROR IN DEFAULTS.PY: DOES COL NAME MATCH .JSON?')

            model.create(**x)

from .models import UserModel
import sched, time
from .. import discord
from .models import *
import datetime
from random import randint

s = sched.scheduler(time.time, time.sleep)
utcnow = datetime.datetime.utcnow()
date = utcnow.date()

units = []
calls = []


def random_id(prefix=None, digits: int = 8):
    _id = randint(10 ** (digits - 1), (10 ** digits) - 1)
    if prefix is not None:
        return f'{prefix}-{_id}'
    return _id


class Call(object):
    def __init__(self, callId, callType: int, subTypeCode: str, postal: int, location: str, description: str):
        self.callId = callId
        self.callType = callType  # {0: 'Police', 1: 'Fire', 2: 'Medical')
        self.subTypeCode = subTypeCode
        self.subType = CallTypeModel.query.filter_by(code=subTypeCode).first().type
        self.postal = postal
        self.location = location
        self.description = description

    @property
    def units(self):
        _l = []
        for i in units:
            if i.currentCall is None:
                continue
            if i.currentCall.callId == self.callId:
                _l.append(i)

        return _l

    def attach(self, unit_id: str):
        """ Attach unit to call """
        unit = item = next((i for i in units if i.unit_id == unit_id), None)
        if unit is None:
            return None


class Unit(object):
    def __init__(self, unit_id: str, dept_id: int, discord_id: str):
        self.unit_id = unit_id
        self.dept_id = dept_id
        self.discord_id = discord_id
        timeout_date = s.enter(28800, 1, self._timeout)

        self.status = 0  # Initial status is 0 (End Tour)
        self.currentCall: Call = None
        self.log: list[tuple] = []  # [("log message", date)]

        self.user: UserModel = UserModel.query.filter_by(discord_id=discord_id).first()

    def _timeout(self):
        """ Remove unit after 8 hours of no activity. """
        self.status = 0


def register_unit(unit_id: str, department_id: int):
    """
    Append unit to units list

    :param unit_id:
    :param department_id:
    :return:
    """

    user = discord.fetch_user()

    unit = next((i for i in units if i.discord_id == discord.fetch_user().id), None)
    if unit is not None:
        units.remove(unit)
        del unit

    unit = Unit(unit_id, department_id, user.id)
    units.append(unit)


def create_call(type: int, subTypeCode: str, postal: int, location: str, description: str):
    callId = f'{date.strftime("%Y")}-{randint(10 ** 7, (10 ** 8) - 1)}'  # Year-12345678

    call = Call(callId=callId, callType=type, subTypeCode=subTypeCode, postal=postal,
                location=location, description=description)
    calls.append(call)

    return call

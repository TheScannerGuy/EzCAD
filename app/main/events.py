from flask_socketio import send, emit, Namespace
from .. import socketio


#  METHOD
#  EzCAD uses a mix of both API and Web Sockets to send data.
#  Using the API is preferred as Web Sockets can be a challenge
#  with the angular framework. Due to this, web sockets should be sent
#  as 'reminders' for the client to refresh the API. For example,
#  when a new unit signs in, the dispatch should receive an event
#  telling them to re-request the /api/unit/all instead of the
#  data being sent through websockets.


@socketio.on('connect')
def on_connect(data):
    pass


def unit_change():
    """ Sent to all clients in order to re-request status via API.
        Should be called after the status of a unit is changed. """

    emit('statusChange', broadcast=True)

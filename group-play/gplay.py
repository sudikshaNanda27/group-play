#!/usr/bin/env python
from flask import Flask, render_template, session, request, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = "\xc2\xf6b\\\xfe_\x05\x0e'\xc8\xa8\x1dQ\xf5\x1f;\xc1\x90\xb2\x0ek/\xac~"
socketio = SocketIO(app, async_mode=async_mode)
thread = None


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/song.mp3')
def  song():
    return send_file('/home/sanket/Downloads/The Chainsmokers - Don\'t Let Me Down ft. Daya [mp3clan.com].mp3')

@socketio.on('play')
def play(message):
    room = message['room']
    print "playing in: " + room
    emit('play',{},room=room)

@socketio.on('pause')
def play(message):
    room = message['room']
    print "pausing in: " + room
    emit('pause',{},room=room)

@socketio.on('stop')
def play(message):
    room = message['room']
    print "stopping in: " + room
    emit('stop',{},room=room)


@socketio.on('my_event')
def test_message(message):
    emit('my_response',
         {'data': message['data']})


@socketio.on('join')
def join(message):
    join_room(message['room'])
    print "joined: " + request.sid
    session['room'] = message['room']
    emit('join_success',
         {'data': 'In rooms: ' + ', '.join(rooms())})


@socketio.on('leave')
def leave(message):
    leave_room(message['room'])
    session['room'] = None
    emit('leave_success',
         {'data': 'In rooms: ' + ', '.join(rooms())})


@socketio.on('close_room')
def close(message):
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.'},
         room=message['room'])
    close_room(message['room'])


@socketio.on('disconnect_request')
def disconnect_request():
    emit('my_response',
         {'data': 'Disconnected!'})
    disconnect()


@socketio.on('my_ping')
def ping_pong():
    emit('my_pong')


@socketio.on('connect')
def test_connect():
    # global thread
    # if thread is None:
    #     thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app,host= '0.0.0.0', debug=True)
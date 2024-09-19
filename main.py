from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages/count')
def message_count():
    return {'count': len(messages)}

@socketio.on('newMessage')
def handle_new_message(message):
    messages.append(message)
    emit('message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

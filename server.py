from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{'text': msg.text, 'time': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages])

@app.route('/messages/count', methods=['GET'])
def count_messages():
    count = Message.query.count()
    return jsonify({'count': count})

@socketio.on('send_message')
def handle_send_message(data):
    new_message = Message(text=data['text'])
    db.session.add(new_message)
    db.session.commit()
    timestamp_str = new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    emit('message', {'text': new_message.text, 'time': timestamp_str}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)

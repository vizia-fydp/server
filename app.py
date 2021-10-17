from flask import Flask, request
from flask_socketio import SocketIO, emit

# Initialize flask app
app = Flask(__name__)

# Configure socket IO
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Homepage URL routing
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        socketio.emit("test", "Hello from Flask SocketIO!")
        return "HELLO"
    else:
        pass

@socketio.on('connect')
def connect():
    print("Succesfully connected")

if __name__ == "__main__":
    socketio.run(app)
import os
import numpy as np
import cv2
from flask import Flask, request
from flask_socketio import SocketIO, emit

# Initialize flask app
app = Flask(__name__)

# Configure socket IO
# enables secure client connection
app.config['SECRET_KEY'] = os.urandom(12)
socketio = SocketIO(app)

# Homepage URL routing
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        socketio.emit("test", "Hello from Flask SocketIO!")
        return "HELLO"
    else:
        data = request.form["msg"]
        print(data)
        socketio.emit("test", data)
        return "Success"

@app.route('/image', methods=['POST'])
def image():
    if request.method == 'POST':
        # convert string of image data to uint8
        nparr = np.frombuffer(request.data, np.uint8)

        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('gray.jpg', gray)

        return "SUCCESS"
    else:
        return "ERROR"

@socketio.on('connect')
def connect():
    print("Succesfully connected")

if __name__ == "__main__":
    socketio.run(app)
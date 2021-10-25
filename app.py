import os
import numpy as np
import cv2
import jsonpickle
from flask import Flask, request, Response
from flask_socketio import SocketIO, emit
from color_detection.detect import detect_color

# Initialize flask app
app = Flask(__name__)

# Configure socket IO
# enables secure client connection
app.config["SECRET_KEY"] = os.urandom(12)
socketio = SocketIO(app)

# Homepage URL routing
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        socketio.emit("test", "Hello from Flask SocketIO!")
        return "HELLO"
    else:
        data = request.form["msg"]
        print(data)
        socketio.emit("test", data)
        return "Success"

@app.route("/detect_color", methods=["POST"])
def image():
    if request.method == "POST":
        # Convert string of image data to uint8
        np_arr = np.frombuffer(request.data, np.uint8)

        # Decode image
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Perform Color detection
        color_name, rgb = detect_color(img)

        # Prepare and return response
        response = {"color_name" : color_name, "rgb" : rgb}
        return Response(
            response = jsonpickle.encode(response),
            status = 200,
            mimetype = "application/json"
        )
    else:
        return "ERROR"

@socketio.on("connect")
def connect():
    print("Succesfully connected")

if __name__ == "__main__":
    socketio.run(app)
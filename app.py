import cv2
import os
import jsonpickle
import numpy as np
from flask import Flask, request, Response
from flask_socketio import SocketIO
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
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Perform color detection
        color_names, rgb_array = detect_color(img, 3)

        # Convert list of colors into one string
        # Eg: ["Red", "Blue", "Green"] -> "Red, Blue, and Green"
        color_text = ""
        if len(color_names) == 1:
            color_text = color_names[0]
        else:
            for idx, color in enumerate(color_names):
                if idx == (len(color_names) - 1):
                    color_text += "and {}".format(color)
                else:
                    color_text += "{}, ".format(color)

        # Prepare and return response
        response = {"colors" : color_text, "rgb" : rgb_array}
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
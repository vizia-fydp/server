import cv2
import json
import jsonpickle
import os
import requests
import socket
import torch
import numpy as np

from flask import Flask, request, Response
from flask_socketio import SocketIO
from pathlib import Path

from color_detection.detect import detect_color, detect_color_2
from money_classification.model_inference import load_model, run_inference


# Initialize flask app
app = Flask(__name__)

# Configure socket IO
# enables secure client connection
app.config["SECRET_KEY"] = os.urandom(12)
socketio = SocketIO(app)

# Use gpu if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Load in money classification model
model = load_model("lucky-sweep-6_best_model.pt", device)


# Homepage URL routing
# Can be used as a liveness check
@app.route("/", methods=["GET", "POST"])
def index():
    return Response(status = 200)


@app.route("/socket_emit", methods=["POST"])
def socket_emit_route():
    """
    Emits a string through SocketIO
    ---

    Data:
        byte string containing message

    Parameters:
        path : String with SocketIO path
        language: (Optional) ISO 639-1 language code
    """
    if request.method == "POST":
        path = request.args.get("path")
        if path is None:
            return Response(status = 400)

        # English default if no language provided
        language = request.args.get("language")
        if language is None:
            language = "en"

        data = {"text": request.data.decode("utf-8"), "language": language}
        # Convert bytes to string and emit on socket
        socketio.emit(path, data)
        return Response(status = 200)
    else:
        return Response(status = 404)


@app.route("/detect_color", methods=["POST"])
def detect_color_route():
    """
    Performs color detection using k-means clustering
    ---

    Data:
        jpg encoded image data

    Parameters:
        k : The number of colors to return. Defaults to 3 if this parameter is
            not provided.
        socket_emit_path : If present, emit results on this socketIO path

    Response:
        colors: A single string with color results in order from
            most dominant to least dominant. Eg: "Red, Green, and Blue" .
        rgb: A list containing the [R, G, B] values for each color detected
    """
    if request.method == "POST":
        # Convert string of image data to uint8
        np_arr = np.frombuffer(request.data, np.uint8)

        # Decode image
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Perform color detection
        k = request.args.get("k")
        try:
            k = 3 if k is None else k
            k = int(k)
        except ValueError:
            return Response(status = 400)
        color_names, rgb_array = detect_color(img, k)

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

        # Prepare response
        response = {"colors" : color_text, "rgb" : rgb_array}

        # Emit on socket if specified
        socket_emit_path = request.args.get("socket_emit_path")
        if socket_emit_path is not None:
            socketio.emit(socket_emit_path, {"text": color_text})

        return Response(
            response = jsonpickle.encode(response),
            status = 200,
            mimetype = "application/json"
        )
    else:
        return Response(status = 404)


@app.route("/detect_color_2", methods=["POST"])
def detect_color_2_route():
    """
    Performs color detection using euclidean distance matching
    ---

    Data:
        jpg encoded image data

    Parameters:
        k : The number of colors to return. Defaults to 3 if this paramter is
            not provided.
        socket_emit_path : If present, emit results on this socketIO path

    Response:
        colors: A single string with color results in order from
            most dominant to least dominant. Eg: "Red, Green, and Blue" .
    """
    if request.method == "POST":
        # Convert string of image data to uint8
        np_arr = np.frombuffer(request.data, np.uint8)

        # Decode image
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Perform color detection
        k = request.args.get("k")
        try:
            k = 3 if k is None else k
            k = int(k)
        except ValueError:
            return Response(status = 400)
        color_names = detect_color_2(img, k)

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

        # Prepare response
        response = {"colors" : color_text}

        # Emit on socket if specified
        socket_emit_path = request.args.get("socket_emit_path")
        if socket_emit_path is not None:
            socketio.emit(socket_emit_path, {"text": color_text})

        return Response(
            response = jsonpickle.encode(response),
            status = 200,
            mimetype = "application/json"
        )
    else:
        return Response(status = 404)


@app.route("/ocr", methods=["POST"])
def ocr_route():
    """
    Performs Optical Character Recognition (OCR) using the Google Cloud
    Vision API (https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate)
    ---

    Data:
        Base64 encoded string of image data

    Parameters:
        type :
            "DOCUMENT_TEXT_DETECTION" for document text,
            "TEXT_DETECTION" for everything else (in-the-wild and handwritten).
            Defaults to "TEXT_DETECTION" if not provided.
        socket_emit_path : If present, emit results on this socketIO path

    Response:
        text: A single string containing all the OCR results
        language: ISO 639-1 language code. Eg: "en" for English, "fr" for French
    """
    if request.method == "POST":
        api_key = Path("ocr/api_key.txt").resolve().read_text()
        detection_type = request.args.get("type")
        detection_type = "TEXT_DETECTION" if detection_type is None else detection_type

        # Prepare request dict
        data = {
            "requests":[{
                "image":{
                    "content": request.data.decode('utf-8')
                },
                "features":[{
                    "type": detection_type
                }]
            }]
        }

        # Make request to google vision api
        endpoint = "https://vision.googleapis.com/v1/images:annotate?key={key}".format(key=api_key)
        google_response = requests.post(endpoint, json=data)

        if google_response.status_code != 200:
            # If we got an error, just return it
            return google_response

        # Convert google api response to json
        r = json.loads(google_response.text)

        # Extract text and language if found in google api response
        txt = "No text detected"
        language = "en"
        if "fullTextAnnotation" in r["responses"][0]:
            txt = r["responses"][0]["fullTextAnnotation"]["text"] \
                .replace("\n", " ")
            language = r["responses"][0]["textAnnotations"][0]["locale"]

        # Prepare response dict
        response = {"text" : txt, "language": language}

        # Emit on socket if specified
        socket_emit_path = request.args.get("socket_emit_path")
        if socket_emit_path is not None:
            socketio.emit(socket_emit_path, response)

        return Response(
            response = jsonpickle.encode(response),
            status = 200,
            mimetype = "application/json"
        )
    else:
        return Response(status = 404)


@app.route("/classify_money", methods=["POST"])
def classify_money():
    """
    Performs money classification on American Bills using resnet50
    trained on a custom dataset.
    ---

    Data:
        jpg encoded image data

    Parameters:
        socket_emit_path : If present, emit results on this socketIO path

    Response:
        predicted_class: One of [1, 5, 10, 20, 50, 100]
    """
    if request.method == "POST":
        # Convert string of image data to uint8
        np_arr = np.frombuffer(request.data, np.uint8)

        # Decode image
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Run inference on image
        prediction = run_inference(model, img, device)

        # Prepare response
        response = {"predicted_class" : prediction}

        # Emit on socket if specified
        socket_emit_path = request.args.get("socket_emit_path")
        if socket_emit_path is not None:
            socketio.emit(socket_emit_path, {"text": str(response["predicted_class"])})

        return Response(
            response = jsonpickle.encode(response),
            status = 200,
            mimetype = "application/json"
        )
    else:
        return Response(status = 404)


@socketio.on("connect")
def connect():
    print("socket connected")


#### Localhost testing ####
if __name__ == "__main__":
    # Find an available port number
    url = "127.0.0.1" # localhost
    port = 0
    with socket.socket() as s:
        s.bind((url, 0))
        port = s.getsockname()[1]

    print("Server running on https://{}:{}".format(url, port))
    socketio.run(app, port=port)

#### Production ####
# if __name__ == "__main__":
#     socketio.run(app)
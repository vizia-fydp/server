# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594
import base64
import json

import requests
import cv2


# URL = "http://127.0.0.1:5000"
URL = "https://3e6b-2607-fea8-1ca4-b000-387e-d423-83cc-135f.ngrok.io"

# SocketIO paths that iOS app listens on
IOS_INFO = "iOS_info"
IOS_RESULTS = "iOS_results"

# Long text for testing speech synthesis
MSG_EN = ("There are roughly 253 million people globally who have some form "
        "of visual impairment. Sighted individuals take for granted the "
        "richness of visual information available to them in order to "
        "navigate the world. We have developed wearable glasses that can "
        "extract, decode, and communicate information from an image to a "
        "visually impaired user through audio transcription. Our system "
        "leverages computer vision to perform optical character "
        "recognition, money classification, and colour detection")


def color_detection_test(filename):
    # prepare headers for http request
    content_type = "image/jpeg"
    headers = {"content-type": content_type}
    params = {"k": 3, "socket_emit_path": IOS_INFO}

    img = cv2.imread(filename)

    # encode image as jpeg
    _, img_encoded = cv2.imencode(".jpg", img)

    # Send request
    response = requests.post(
        url = "{}/detect_color".format(URL),
        data = img_encoded.tobytes(),
        headers = headers,
        params = params
    )

    if response.status_code != 200:
        print("detect_color error")
    else:
        return json.loads(response.text)


def ocr_test(filename):
    # prepare headers for http request
    content_type = "image/jpeg"
    headers = {"content-type": content_type}
    params = {"type": "TEXT_DETECTION", "socket_emit_path": IOS_RESULTS}

    # Load image and encode as base64 string
    img = cv2.imread(filename)
    _, img_arr = cv2.imencode('.jpg', img)
    img_bytes = img_arr.tobytes()
    encoded_img = base64.b64encode(img_bytes)

    # Send request
    response = requests.post(
        url = "{}/ocr".format(URL),
        data = encoded_img,
        headers = headers,
        params = params
    )

    if response.status_code != 200:
        print("ocr error")
        print(response.text)
    else:
        return json.loads(response.text)


def money_classification_test(filename):
    # prepare headers for http request
    content_type = "image/jpeg"
    headers = {"content-type": content_type}
    params = {"socket_emit_path": IOS_INFO}

    img = cv2.imread(filename)

    # encode image as jpeg
    _, img_encoded = cv2.imencode(".jpg", img)

    # Send request
    response = requests.post(
        url = "{}/classify_money".format(URL),
        data = img_encoded.tobytes(),
        headers = headers,
        params = params
    )

    return json.loads(response.text)


def socket_test(path, msg, language):
    params = {"path": path, "language" : language}
    requests.post(
        url = "{}/socket_emit".format(URL),
        data = msg,
        params = params
    )


if __name__ == "__main__":
    # Color det test
    response = color_detection_test("test_images/color_detection/flowers.jpg")
    print(response)

    # OCR test
    response = ocr_test("test_images/ocr/eardrops.jpg")
    print(response)

    response = ocr_test("test_images/color_detection/leaves.jpg")
    print(response)

    # Money classification test
    response = money_classification_test("test_images/money_classification/100.jpeg")
    print(response)

    # Socket tests in various languages
    # socket_test("iOS_info", MSG_EN, "en")
    # socket_test("iOS_results", MSG_EN, "en")
    # socket_test("iOS_results", "Bonjour Monsieur comment allez vous", "fr")
    # socket_test("iOS_results", "?????????? ???? ???????? ?????? ????????".encode("utf-8"), "ar")
    # socket_test("iOS_results", "Hallo, Herr, wie geht es Ihnen?", "de")

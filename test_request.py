# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594
import base64
import json

import requests
import cv2


#URL = "http://127.0.0.1:5000"
URL = "http://9b58-2607-fea8-1ba3-6a00-cdb1-7977-f830-77df.ngrok.io"


def color_detection_test(filename):
    # prepare headers for http request
    content_type = "image/jpeg"
    headers = {"content-type": content_type}

    # img = cv2.imread("img/lego.png")
    img = cv2.imread(filename)

    # encode image as jpeg
    _, img_encoded = cv2.imencode(".jpg", img)

    # Send request
    response = requests.post(
        url = "{}/detect_color".format(URL),
        data = img_encoded.tobytes(),
        headers = headers
    )

    return json.loads(response.text)

def ocr_test(filename):
    # prepare headers for http request
    content_type = "image/jpeg"
    headers = {"content-type": content_type}

    with open(filename, 'rb') as img_file:
        img_content = img_file.read()
    encoded_img = base64.b64encode(img_content)

    # Send request
    response = requests.post(
        url = "{}/ocr".format(URL),
        data = encoded_img,
        headers = headers
    )

    return json.loads(response.text)


if __name__ == "__main__":
    ### Color det test
    response = color_detection_test("test_images/color_detection/flowers.jpg")
    print(response)

    ### OCR test
    response = ocr_test("test_images/ocr/eardrops.jpg")
    print(response)

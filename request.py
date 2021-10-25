# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

import requests
import json
import cv2

URL = "http://127.0.0.1:5000"
# URL = "https://33b0-2601-646-c200-cb40-c119-df75-41e7-9bac.ngrok.io"

if __name__ == "__main__":
    # data = {"msg": "Oscar Nespoli"}
    # requests.post(url = URL, data = data)

    # prepare headers for http request
    content_type = "image/jpeg"
    headers = {"content-type": content_type}

    img = cv2.imread("img/lego.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # encode image as jpeg
    _, img_encoded = cv2.imencode(".jpg", img)

    # Send request
    response = requests.post(
        url = "{}/detect_color".format(URL),
        data = img_encoded.tobytes(),
        headers = headers
    )

    print(json.loads(response.text))
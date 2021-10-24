import requests

URL = "http://127.0.0.1:5000"
# URL = "https://33b0-2601-646-c200-cb40-c119-df75-41e7-9bac.ngrok.io"

if __name__ == "__main__":
    # data = {"msg": "Oscar Nespoli"}
    # requests.post(url = URL, data = data)

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    img = open("img/eardrops.jpg", 'rb').read()
    requests.post(url = "{}/image".format(URL), data=img, headers=headers)
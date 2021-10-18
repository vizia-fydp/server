import requests

URL = "http://127.0.0.1:5000"
# URL = "http://127.0.0.1"

if __name__ == "__main__":
    data = {"msg": "Oscar Nespoli"}
    requests.post(url = URL, data = data)
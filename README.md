# Server
The Vizia server is responsible for all of the AI inference logic as well as forwarding the results to the iOS app. The server provides APIs for optical character recognition, colour detection, and US money detection.

## APIs
* `/socket_emit`: Emits a string on a specified socket. Used to communicate state changes from the glasses to the iOS app.
* `/ocr`: Performs Optical Character Recognition (OCR) using the Google Cloud Vision API.
* `/detect_color`: Performs color detection using k-means clustering.
* `/detect_color_2`: Performs color detection using euclidean distance matching.
* `/classify_money`: Performs money classification using a Resnet50-CNN.

## Setup
Dependencies to run the server can be installed using either conda or python virtual environments.

#### Conda
Install miniconda and create environment from given file:
```
conda env create -f environment.yml
```

#### Virtual env
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

#### Google Cloud Vision API Setup
To be able to perform OCR, an API key is needed for the Google Cloud Vision API. A Google account is first needed before proceeding. Then, complete the first 3 steps on the [setup page](https://cloud.google.com/vision/docs/setup) (Create a project, Enable billing, Enable the API). In your Google Cloud Console, go to APIs & Services using the navigation menu and then Credentials. Create a new API key and copy it to your clipboard. Store it using an environment variable on the machine you will be running the server with, using the following command (adding the command to the machine's bashrc file is recommended):
```
export GC_VISION_API_KEY="<api_key>"
```

## Running the server
```
python3 app.py
```
By default, the server will run on `localhost`.

#### Localhost tunneling with `ngrok`
```
ngrok http <port>
```
`ngrok` is a useful free tool for localhost tunnelling, which provides a URL that can be used to access the server from other machines.

#### Production
For a more permanent solution, it would be best to use something like Amazon EC2. We tried to use AWS Lambda and Heroku, but had deployment problems with both.

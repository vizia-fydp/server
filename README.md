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
conda env create -f gpu_environment.yml
```

Or if using CPU:
```
conda env create -f cpu_environment.yml
```

If that fails, create a new env with Python 3.9 and install the following libraries:
```
conda create -n fydp-server python=3.9
conda config --add channels conda-forge
conda install pytorch torchvision cudatoolkit=11.1 -c pytorch -c nvidia
conda install -c conda-forge jsonpickle opencv flask requests flask-socketio pandas gevent-websocket eventlet
```

If using CPU instead of GPU, run the following command instead of the other pytorch command:
```
conda install pytorch torchvision cpuonly -c pytorch
```

#### Virtual env
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
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
For a more permanent solution, it would be best to use something like Amazon EC2. We tried to use AWS Lambda and Heroku, but had problems with both. (Too big for AWS Lambda, and deployment issues with Heroku)

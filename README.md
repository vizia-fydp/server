# server

Install miniconda and create environement from given file:
`conda env create -f environment.yml`

If that fails, create a new env with Python 3.9 and install the following libraries:
`conda create -n fydp-server python=3.9`
`conda config --add channels conda-forge`
`conda install jsonpickle opencv flask requests flask-socketio pandas`

To run server on localhost:
`python3 app.py`

Install ngrok using:
`sudo apt-get update`
`sudo snap install ngrok`

Localhost tunneling with `ngrok`:
`ngrok http <port>`

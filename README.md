# Server

## Setup

Install miniconda and create environement from given file:

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
conda install -c conda-forge jsonpickle opencv flask requests flask-socketio pandas
```

If using CPU instead of GPU, run the following command instead of the other pytorch command:

```
conda install pytorch torchvision cpuonly -c pytorch
```

Install ngrok using:

```
sudo apt-get update
sudo snap install ngrok
```

## Running

To run server on localhost:

```
python3 app.py
```

Localhost tunneling with `ngrok`:

```
ngrok http <port>
```

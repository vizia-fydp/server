# Server

## Setup

Install miniconda and create environement from given file:

```
conda env create -f environment.yml
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

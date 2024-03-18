#!/bin/bash


# check if venv directory exists
if [ -d "venv" ]; then
  echo 'Error: venv directory already exists.' >&2
  echo 'Please remove the venv directory and run the setup.sh script again.'
  exit 1
fi

python3 -m venv venv

# Activate virtual environment
source venv/bin/activate


# Install requirements
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev -y
pip install -r requirements.txt


# Run the app with gunicorn
gunicorn app:app --bind "0.0.0.0"

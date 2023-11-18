#!/bin/bash

python3 -m venv venv

source venv/bin/activate

pip3 install black pytest boto3 moto

black src/ tests/

export PYTHONPATH="$(pwd)/src/api_handler:$PYTHONPATH"

if pytest; then
  deactivate
  exit 0
else
  deactivate
  exit 1
fi
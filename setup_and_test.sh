#!/bin/bash

python3 -m venv venv

source venv/bin/activate

pip3 install black pytest boto3

black src/ tests/

export PYTHONPATH="$(pwd)/src/api_handler:$PYTHONPATH"

pytest

deactivate

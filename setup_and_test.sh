#!/bin/bash

export PYTHONPATH="$(pwd)/src/api_handler:$PYTHONPATH"

coverage_test=false
html_report=false

usage() {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  --coverage   Run coverage tests"
  echo "  --html       Generate an HTML coverage report (requires --coverage)"
  echo "  --help       Display this help message"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --coverage)
      coverage_test=true
      ;;
    --html)
      html_report=true
      ;;
    --help)
      usage
      ;;
    *)
      echo "Unknown option: $1"
      usage
      ;;
  esac
  shift
done

python3 -m venv venv
source venv/bin/activate

pip3 install black pytest boto3 moto

black src/ tests/

if [ "$coverage_test" = true ]; then
  pip3 install coverage

  coverage run -m pytest

  if [ "$html_report" = true ]; then
    coverage html

    open htmlcov/index.html
    if [ $? -ne 0 ]; then
      echo "HTML report cannot be opened. Please open \"htmlcov/index.html\" manually."
    fi
  else
    coverage report
  fi
else
  pytest
fi

if [ $? -eq 0 ]; then
  deactivate
  exit 0
else
  deactivate
  exit 1
fi
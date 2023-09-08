#!/usr/bin/env bash
python -m venv ./venv
source ./venv/Scripts/activate
cd ./auto_getter || exit
pip install -r requirements.txt
python ./main.py
cd ..
# deactivate

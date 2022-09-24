#!/usr/bin/env bash
source ./venv/Scripts/activate
cd ./auto_getter || exit
pip install -r requirements.txt
python ./main.py

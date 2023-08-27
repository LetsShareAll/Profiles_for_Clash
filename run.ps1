python -m venv ./venv
./venv/Scripts/activate.ps1
Set-Location ./auto_getter
pip install -r requirements.txt
python ./main.py
Set-Location ..
deactivate

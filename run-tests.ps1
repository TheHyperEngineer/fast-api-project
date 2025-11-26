# Run pytest in the repo
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q --disable-warnings

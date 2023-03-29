python -m pip install flask
python -m pip install markdown

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=False

python -m flask run
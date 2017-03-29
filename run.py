# On Cloud9:
# pip install -r requirements.txt
# export FLASK_APP=run.py
# flask run --host '0.0.0.0' --port '8080' 

from app import app 

if __name__ == "__main__":
    app.run()
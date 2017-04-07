# On Cloud9:
# pip install -r requirements.txt
# export FLASK_APP=run.py
# flask run --host '0.0.0.0' --port '8080' 

import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
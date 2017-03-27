# On Cloud9:
# flask run --host '0.0.0.0' --port '8080' 

from app import app 

# Uncomment this in production
# TODO figure out where this should go...?
# application = app

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))

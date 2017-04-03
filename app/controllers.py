# Controllers for manipulating models

from flask import request, jsonify
from app import app
import helpers

# TODO this should check that the user is logged in.
@app.route('/forms/continuation', methods=['POST'])
def newContinuationForm():
    data = request.get_json() # Get POSTed JSON from Javascript
    
    # Check endorsement area
    endorsementArea = helpers.getEndorsementArea(data['endorsementArea'])
    if (endorsementArea == 0):
        return jsonify({'Failure':'Endorsement Area is invalid.'})
    # Check the test requirements have valid tests and dates
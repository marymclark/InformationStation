# Controllers for manipulating models

from flask import request, jsonify
from app import app
import helpers

# TODO this should check that the user is logged in.
@app.route('/forms/continuation', methods=["POST"])
def newContinuationForm():
    try:
        data = request.get_json() # Get POSTed JSON from Javascript
    except:
        return jsonify({'Failure':'No request data.'})
    
    # Check endorsement area
    for endorsement in data['endorsementArea']:
        endorsementArea = helpers.getEndorsementArea(endorsement)
        if (endorsementArea == 0):
            return jsonify({'Failure':'An endorsement area is invalid.'})
            
    # Check the test requirements have valid tests and dates
    for item in data['testRequirements']:
        # TODO check date
        date = item['date']
        if not (item['exam'] in ['Praxis','VCLA','RVE']):
            return jsonify({'Failure':'A test requirement entry is invalid.'})
            
    # Check graduation
    checkGrad = data['graduation'].split()
    if not ((checkGrad[0] in ['May','August','December']) and (checkGrad[1] in helpers.nextnYears(5))):
        jsonify({'Failure':'Invalid graduation month/year'})
        
    # Add data to database
    # TODO add to database
    
    # For now, return success when valid 
    return jsonify({'Success':'Request was valid.'})
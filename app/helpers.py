# Helper functions for the application.

import datetime
from json import load
from functools import wraps
from flask_login import current_user
from flask import abort

# Decorator for admin-restricted pages.
def admin_required(func):
    @wraps(func)
    def check_admin_and_call(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return check_admin_and_call

# Get the next n years for a form
def nextnYears(n):
    year = datetime.datetime.now().year
    return [year+i for i in range(0,n)]
    
# Get the file for endorsement areas
def getEndorsements():
    try:
        with open('app/data/endorsements.json') as file:
            return load(file)
    except IOError:
        return ({"error": "Failed to get file"})
        
# Get the file for schools
def getSchools():
    try:
        with open('app/data/schools.json') as file:
            return load(file)
    except IOError:
        return ({"error": "Failed to get file"})

# Get the endorsement from an index
def getEndorsementArea(key):
    endorsements = getEndorsements()['data']
    key = [i for i in key if i is not None] # Remove None values; remaining 1-3 values should cooardinate to endorsementarea
    endorsementArea = ''
    try:
        for i in range(0,len(key)):
            endorsementArea += (endorsements[key[i]]['title'])
            if i < len(key)-1:
                endorsementArea += ', '
                endorsements = endorsements[key[i]]['subcategories']
        return endorsementArea 
    except:
        print('Error getting endorsementArea; found: "'+endorsementArea+'"')
        return 0
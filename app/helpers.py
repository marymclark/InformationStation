# Helper functions for the mvc

import datetime
from json import load

# Get the next n years for a form
def nextnYears(n):
    year = datetime.datetime.now().year
    return [year+i for i in range(0,n)]
    
def getEndorsements():
    try:
        with open('app/data/endorsements.json') as file:
            return load(file)
    except:
        return ({"error": "Failed to get file"})
        
def getEndorsementArea(key):
    endorsements = getEndorsements()['data']
    endorsementArea = ''
    try:
        for i in range(0,len(key)):
            endorsementArea += (endorsements[key[i]]['title'])
            if i < len(key)-1:
                endorsementArea += ', '
                endorsements = endorsements[key[i]]['subcategories']
        return endorsementArea 
    except:
        print('Error getting endorsementArea; so far: "'+endorsementArea+'"')
        return 0
        
def getSchools():
    try:
        with open('app/data/schools.json') as file:
            return load(file)
    except:
        return ({"error": "Failed to get file"})
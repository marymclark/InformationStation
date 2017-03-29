// Form stuff

// Iterator to travel JSON object
function travel(obj,level) {
    for (var key in obj) {
        /*if (typeof obj[key] == "object" && obj[key] !== null) {
            level = level + 1;
            data = travel(obj[key], level);
            append.
        }
        else { 
            return {'level':level,'name':obj[key]}; 
        }*/
        console.log(obj[key]);
    }
}

// TODO this needs to take asynchronous callback
function buildEndorsementArea() {
    // Import JSON object with endorsements
    $.getJSON("/api/endorsements", function(data) {
        // Travel through list
        travel(data['data'],0);
        //console.log(result);
    });
}

// Run
$(document).ready(function() {
    if ($('#endorsementArea').length) { // If an endorsement area is needed
        buildEndorsementArea(); // Build all of the dropdown boxes for it
    }
});
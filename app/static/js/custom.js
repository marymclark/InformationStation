// Form Functions

// TODO this needs to take asynchronous callback
function buildEndorsementArea() {
    // Import JSON object with endorsements
    $.getJSON("/api/endorsements", function(data) {
        // Get the first level
        
        // Create a dropdown from that first level
        
        // Now listen for the value in the dropdown to change
        
        // When something in the first level is chosen, 
        // update a second dropdown with the first level's subcategories
        
        // When something in the second level is chosen,
        // update a third dropdown with the first level's subcategories
    });
}

// Run
$(document).ready(function() {
    if ($('#endorsementArea').length) { // If an endorsement area is needed
        buildEndorsementArea(); // Build all of the dropdown boxes for it
    }
});
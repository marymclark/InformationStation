// Form Functions

// TODO this needs to take asynchronous callback
function buildEndorsementArea() {
    // Import JSON object with endorsements
    $.getJSON("/api/endorsements", function(data) {
        // Get the first level
        data = data['data']; // Get the actual data we need
        
        var first_level = [];
        for (var key in data) {
            first_level.push([data[key].title, key]); // key seems redundant but I promise I'm trying something here
        }
        console.log(first_level);
        
        // Create a dropdown from that first level
        $("#endorsementArea").append('<div class="col-sm-4"><select class="form-control" id="endorsementArea1"></select></div>');
        for (var key in first_level) {
            $("#endorsementArea1").append('<option value="'+first_level[key][1]+'">'+first_level[key][0]+'</option>');
        }
        
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
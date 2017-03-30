// Form Functions

// TODO once this is worked out and runs okay, needs to be refactored
function buildEndorsementArea() {
    // Import JSON object with endorsements
    $.getJSON("/api/endorsements", function(data) {
        // Get the first level
        data = data['data']; // Get the actual data we need
        
        var first_level = [];
        for (var key in data) {
            first_level.push(data[key].title);
        }
        console.log("first_level:"+first_level);
        
        // Create a dropdown from that first level
        $("#endorsementArea").append('<div class="col-sm-4"><select class="form-control" id="endorsementArea1"></select></div>');
        for (var key in first_level) {
            $("#endorsementArea1").append('<option value="'+key+'">'+first_level[key]+'</option>');
        }
        
        // Now listen for the value in the dropdown to change
        // When something in the first level is chosen, 
        // update a second dropdown with the first level's subcategories
        $("#endorsementArea1").change(function() {
            var index1 = $("#endorsementArea1").val();
            let selection = data[index1]; 
            if (selection.subcategories != undefined) { // If subcategories exist
                // Build second_level
                var second_level = [];
                for (var key in selection.subcategories) {
                    second_level.push(selection.subcategories[key].title);
                }
                console.log("second_level:"+second_level);
                
                // Create if doesn't already exist
                if (!$('#endorsementArea2').length) { // If endorsementarea2 isn't already there
                    $("#endorsementArea").append('<div class="col-sm-4"><select class="form-control" id="endorsementArea2"></select></div>');
                }
                
                // Empty and add new elements
                $("#endorsementArea2").empty();
                $("#endorsementArea2").show();
                if ($('#endorsementArea3').length) {
                    $("#endorsementArea3").empty();
                    $("#endorsementArea3").hide();
                }
                for (var key in second_level) {
                    $("#endorsementArea2").append('<option value="'+key+'">'+second_level[key]+'</option>');
                }
                
                // Listen for changes in the second area
                // When something in the second level is chosen,
                // update a third dropdown with the first level's subcategories
                $("#endorsementArea2").change(function() {
                    var index2 = $("#endorsementArea2").val();
                    let selection = data[index1].subcategories[index2]; 
                    if (selection.subcategories != undefined) {
                        var third_level = [];
                        for (var key in selection.subcategories) {
                            third_level.push(selection.subcategories[key].title);
                        }
                        console.log("third_level:"+third_level);
                        
                        // Create if doesn't already exist
                        if (!$('#endorsementArea3').length) { // If endorsementarea2 isn't already there
                            $("#endorsementArea").append('<div class="col-sm-4"><select class="form-control" id="endorsementArea3"></select></div>');
                        }
                        
                        // Empty and add new elements
                        $("#endorsementArea3").empty();
                        $("#endorsementArea3").show();
                        for (var key in third_level) {
                            $("#endorsementArea3").append('<option value="'+key+'">'+third_level[key]+'</option>');
                        }
                    }
                    else {
                        console.log("No subcategories.");
                        // Clear and Hide
                        $("#endorsementArea3").empty();
                        $("#endorsementArea3").hide();
                    }
                });
            } 
            else {
                console.log("No subcategories.");
                // Clear
                $("#endorsementArea2").empty();
                $("#endorsementArea2").hide();
                if ($('#endorsementArea3').length) {
                    $("#endorsementArea3").empty();
                    $("#endorsementArea3").hide();
                }
                // Hide the dropdown
            }
        });
    });
}

// Run
$(document).ready(function() {
    if ($('#endorsementArea').length) { // If an endorsement area is needed
        buildEndorsementArea(); // Build all of the dropdown boxes for it
    }
});
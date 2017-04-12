// Form Functions

// TODO refine and refactor
function buildEndorsementArea() {
    // Import JSON object with endorsements
    $.getJSON("/data/endorsements", function(data) {
        // Build the first level
        data = data['data']; 
        var first_level = [];
        for (var key in data) {
            first_level.push(data[key].title);
        }
        
        // Create dropdowns
        $("#endorsementArea tbody").append('<tr><td><select class="form-control" name="area" id="area"></td></tr>');
        $("#endorsementArea tbody tr").append('<td><select class="form-control" name="subject" id="subject"></select></td>');
        $("#endorsementArea tbody tr").append('<td><select class="form-control" name="subcategory" id="subcategory"></select></td>');
        $("#endorsementArea tbody tr").append('<td>X</td>'); //TODO replace this with an actual button of some kind
        // Add first level
        for (var key in first_level) {
            $("#area").append('<option value="'+key+'">'+first_level[key]+'</option>');
        }
        
        // Now listen for the value in the dropdown to change
        $("#area").change(function() {
            var index1 = $("#area").val();
            let selection = data[index1]; 
            if (selection.subcategories != undefined) { // If subjects exist
                // Build second_level
                var second_level = [];
                for (var key in selection.subcategories) {
                    second_level.push(selection.subcategories[key].title);
                }
                
                // Empty and add new elements
                $("#subject").empty();
                $("#subcategory").empty();
                for (var key in second_level) {
                    $("#subject").append('<option value="'+key+'">'+second_level[key]+'</option>');
                }
                
                // Listen for changes in the second area
                $("#subject").change(function() {
                    var index2 = $("#subject").val();
                    let selection = data[index1].subcategories[index2]; 
                    if (selection.subcategories != undefined) { // If subcategories exist
                        var third_level = [];
                        for (var key in selection.subcategories) {
                            third_level.push(selection.subcategories[key].title);
                        }
                        
                        // Empty and add new elements
                        $("#subcategory").empty();
                        for (var key in third_level) {
                            $("#subcategory").append('<option value="'+key+'">'+third_level[key]+'</option>');
                        }
                    }
                    else {
                        // Clear
                        $("#subcategory").empty();
                    }
                });
            } 
            else {
                // Clear
                $("#subject").empty();
                $("#subcategory").empty();
            }
        });
    });
}

// TODO add more error checking and returning 
$("form.continuation").submit(function(event) {
    event.preventDefault(); // Don't submit yet, build JSON first
    var data = {};
    
    // EndorsementArea
    data["endorsementArea"] = [];
    $("#endorsementArea tbody tr").each(function (i,row) {
        let key = [];
        key.push(Number($(row).find("#area option:selected").val()));
        key.push(Number($(row).find("#subject option:selected").val())); 
        key.push(Number($(row).find("#subcategory option:selected").val()));
        data["endorsementArea"].push(key);
    });
    // Tests
    data["testRequirements"] = [];
    if ($("input[name='tests']:checked").val() == "true") {
        $("#testsRemaining tbody tr").each(function (i,row) {
            let test = {"exam": $(row).find("#examName option:selected").val(),
                        "date": $(row).find("#examDate").val()};
            data["testRequirements"].push(test);
        });
    }
    // Graduation
    data["graduation"] = $("#graduation-Month option:selected").val() + " " + $("#graduation-Year option:selected").val();
    // Continue/Reason
    data["continue"] = $("input[name='continue']:checked").val();
    if (data["continue"] == "true") {
        data["continue"] = true;
        data["reason"] = null;
    }
    else if (data["continue"] == "false") {
        data["continue"] = false;
        data["reason"] = $("input[name='reason']:checked").val();
    }
    else {
        console.log("Error: No continue option selected");
    }
    
    console.log(JSON.stringify(data));
    
    // IF no errors, submit JSON as POST request.
    $.ajax({
        url:"/forms/continuation",
        type:"POST",
        data:JSON.stringify(data),
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success: function(result) {
            console.log(result);
        }
    });
});

// Run
$(document).ready(function() {
    
    // If an endorsementArea exists, add its data
    if ($('table#endorsementArea').length) { 
        buildEndorsementArea(); 
    }
    
    // Add testsRemaining animation
    if ($('#tests').length) { 
        $("#testsToggle").hide();
        $("input[name='tests']").change(function() {
            let val = $("input[name='tests']:checked").val();
            //console.log(val);
            if (val=='true') {
                 $("#testsToggle").show();
            } 
            else {
                $("#testsToggle").hide();
            }
        });
    }
    
    // Add continuing animation
    if ($('#continue').length) { 
        $("#continueToggle").hide();
        $("input[name=continue]").change(function() {
            let val = $("input[name=continue]:checked").val();
            //console.log(val);
            if (val=='false') {
                 $("#continueToggle").show();
            } 
            else {
                $("#continueToggle").hide();
            }
        });
        
    }
});
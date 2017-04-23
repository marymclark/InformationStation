// School Grades list

var school_list = [
    "Pre-K",
    "Kindergarten",
    "First Grade",
    "Second Grade",
    "Third Grade",
    "Fourth Grade",
    "Fifth Grade",
    "Sixth Grade",
    "Seventh Grade",
    "Eigth Grade",
    "Ninth Grade",
    "Tenth Grade",
    "Eleventh Grade",
    "Twelfth Grade",
    "Other"
];

function redirect(route) {
    window.location = route;
}

// Table Functions

function addRow(target) {
    console.log(typeof target);
    var i = 0;
    $(target).append('<tr></tr>');
    
    // Find the nearest row and copy its columns (without values)
    var columns = $(target).find("tr:first").find("td");
    for (i=0; i<columns.length-1; i++) {
        let newColumn = $(columns[i]).clone();
        $(target).find("tr:last").append(newColumn);
    }
    // Add delete button
    $(target).find("tr:last").append('<td><button type="button" class="btn delRow"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td></tr>'); 
}

function delRow(target) {
    console.log(target);
    target.remove();
}


// Form elements

function buildRelationships() {
    $("#relationships tbody").append('<tr><td><input type="text" class="form-control" name="name" id="name"></td></tr>');
    $("#relationships tbody tr").append('<td><select class="form-control" name="rel-district" id="rel-district"></select></td>');
    $("#relationships tbody tr").append('<td><select class="form-control" name="rel-school" id="rel-school"></select></td>');
    $("#relationships tbody tr").append('<td><select class="form-control" name="relationship" id="relationship"></select></td>');
    $("#relationships tbody tr").append('<td><button type="button" class="btn delRow"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td>');   
    
    // Add relationships
    let relationships = ['Parent','Child','Sibling','Spouse','Relative','Friend','Other'];
    for (var rel in relationships) {
        $("select#relationship").append('<option value="'+relationships[rel]+'">'+relationships[rel]+'</option>');
    }
    
    $.getJSON("/data/schools", function(data) {
        data = data['data'];
        let first_level = [];
        for (var key in data) {
            first_level.push(data[key].district);
        }
        
        // Add first level
        console.log($("#rel-district"));
        for (var key in first_level) {
            $("#rel-district").append('<option value="'+key+'">'+first_level[key]+'</option>');
        }
        
        $("#rel-district").change(function() {
            let index1 = $("#rel-district").val();
            let selection = data[index1]; 
            $("#rel-school").empty();
            
            if (selection.schools != undefined) { // If schools exist
                // Build second_level
                let second_level = [];
                for (var key in selection.schools) {
                    second_level.push(selection.schools[key].school);
                }
                
                // Empty and add new elements
                for (var key in second_level) {
                    $("#rel-school").append('<option value="'+key+'">'+second_level[key]+'</option>');
                }
            } 
            else {
                // Clear
                console.log("Nothing to fill");
            }
        });
    });
}

function buildPracticum() {
    // Add elements
    $("#practicum tbody").append('<tr><td><select class="form-control" name="district" id="district"></td></tr>');
    $("#practicum tbody tr").append('<td><select class="form-control" name="school" id="school"></select></td>');
    $("#practicum tbody tr").append('<td><select class="form-control" name="grades" id="grades"></select></td>');
    $("#practicum tbody tr").append('<td><select class="form-control" name="subjects" id="subjects"></select></td>');
    $("#practicum tbody tr").append('<td><button type="button" class="btn delRow"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td>');
    
    // Fill the subjects column
    $.getJSON("/data/endorsements", function(data) {
        data = data['data'];
        var subjects = [];
        // TODO add subcategories into this dropdown as well.
        for (var x in data) {
            let temp = data[x]['subcategories'];
            for (var y in temp) {
                let subject = temp[y]['title'];
                if (subjects.indexOf(subject) < 0) { //TODO this won't work in IE.
                    subjects.push(subject);
                }
            }
        }
        for (var key in subjects) {
            $("#subjects").append('<option value="'+subjects[key]+'">'+subjects[key]+'</option>');
        }
    });
    
    $.getJSON("/data/schools", function(data) {
        data = data['data'];
        let first_level = [];
        for (var key in data) {
            first_level.push(data[key].district);
        }
        
        // Add first level
        for (var key in first_level) {
            $("#practicum #district").append('<option value="'+key+'">'+first_level[key]+'</option>');
        }
        
        $("#practicum #district").change(function() {
            let index1 = $("#practicum #district").val();
            let selection = data[index1]; 
            $("#practicum #school").empty();
            $("#practicum #grades").empty();
            
            if (selection.schools != undefined) { // If schools exist
                // Build second_level
                let second_level = [];
                for (var key in selection.schools) {
                    second_level.push(selection.schools[key].school);
                }
                
                // Empty and add new elements
                for (var key in second_level) {
                    $("#practicum #school").append('<option value="'+key+'">'+second_level[key]+'</option>');
                }
                
                // Listen for changes in the second district
                $("#practicum #school").change(function() {
                    $("#practicum #grades").empty();
                    let index2 = $("#practicum #school").val();
                    let third_level;
                    let selection = data[index1].schools[index2]; 
                    
                    //TODO this problem: looping through every index1 that
                    //has been previously chosen -- why?
                    //console.log(index1 + " " + index2);
                    //console.log(selection);
                    
                    if (selection.school.includes("Elementary")) {
                        third_level = school_list.slice(0,7);
                    }
                    if (selection.school.includes("Middle")) {
                        third_level += school_list.slice(7,10);
                    }
                    if (selection.school.includes("High")) {
                        third_level += school_list.slice(10,school_list.length-1);
                    }
                    if (third_level.length == 0) {
                        console.log("No grade levels available -- provide all options");
                        third_level = school_list;
                    }
                    
                    for (var key in third_level) {
                        $("#practicum #grades").append('<option value="'+key+'">'+third_level[key]+'</option>');
                    }
                });
            } 
            else {
                // Clear
                console.log("Nothing to fill");
            }
        });
    });
}

// TODO refine and refactor
function buildEndorsementArea() {
    // Create dropdowns
    $("#endorsementArea tbody").append('<tr><td><select class="form-control" name="area" id="area"></td></tr>');
    $("#endorsementArea tbody tr").append('<td><select class="form-control" name="subject" id="subject"></select></td>');
    $("#endorsementArea tbody tr").append('<td><select class="form-control" name="subcategory" id="subcategory"></select></td>');
    $("#endorsementArea tbody tr").append('<td><button type="button" class="btn delRow"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td>');
    
    // Import JSON object with endorsements
    $.getJSON("/data/endorsements", function(data) {
        // Build the first level
        data = data['data']; 
        var first_level = [];
        for (var key in data) {
            first_level.push(data[key].title);
        }
    
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

$("form.internship").submit(function(event) {
    event.preventDefault(); // Don't submit yet
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
    if ($("input[name='tests']:checked").val() == "true") {
        data["tests"] = true;   
    }
    else {
        data["tests"] = false;
    }
    
    // Practicums
    data["practicums"] = [];
    $("#practicum tbody tr").each(function (i,row) {
        let practicum = {};
        practicum['division']=$(row).find("#district option:selected").text();
        practicum['school']=$(row).find("#school option:selected").text(); 
        practicum['grade']=$(row).find("#grades option:selected").text();
        practicum['subject']=$(row).find("#subject option:selected").text();
        data["practicums"].push(practicum);
    });
    
    // Relationships
    data["relationships"] = [];
    $("#relationships tbody tr").each(function (i,row) {
        let relationship = {};
        relationship['name']=$(row).find("input#name").val();
        relationship['district']=$(row).find("#rel-district option:selected").text(); 
        relationship['school']=$(row).find("#rel-school option:selected").text();
        relationship['rel']=$(row).find("#relationship option:selected").text();
        data["relationships"].push(relationship);
    });
    
    console.log(JSON.stringify(data));
    
    // IF no errors, submit JSON as POST request.
    $.ajax({
        url:"/forms/internship",
        type:"POST",
        data:JSON.stringify(data),
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success: function(result) {
            alert(result['message']);
            if (result["status"] == "Success") {
                // Redirect to dashboard
                redirect("/dashboard");
            }
        }
    });
});

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
            // TODO .val() below is getting the text inside input and NOT the value like it should
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
        return;
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
            alert(result['message']);
            if (result["status"] == "Success") {
                // Redirect to dashboard
                redirect("/dashboard");
            }
        }
    });
});

//
// Updates "Select all" control in a data table
//

function deleteUser(){
    console.log('deteling datboi')
}
function updateDataTableSelectAllCtrl(table){
   var $table             = table.table().node();
   var $chkbox_all        = $('tbody input[type="checkbox"]', $table);
   var $chkbox_checked    = $('tbody input[type="checkbox"]:checked', $table);
   var chkbox_select_all  = $('thead input[name="select_all"]', $table).get(0);

   // If none of the checkboxes are checked
   if($chkbox_checked.length === 0){
      chkbox_select_all.checked = false;
      if('indeterminate' in chkbox_select_all){
         chkbox_select_all.indeterminate = false;
      }

   // If all of the checkboxes are checked
   } else if ($chkbox_checked.length === $chkbox_all.length){
      chkbox_select_all.checked = true;
      if('indeterminate' in chkbox_select_all){
         chkbox_select_all.indeterminate = false;
      }

   // If some of the checkboxes are checked
   } else {
      chkbox_select_all.checked = true;
      if('indeterminate' in chkbox_select_all){
         chkbox_select_all.indeterminate = true;
      }
   }
}

// Run
$(document).ready(function() {
    
    
    $("#userbacbutton").click(function(){
        
        event.preventDefault();
        
        console.log('bac pushpush')
        
        var isDisabled = $("#userbacbutton").prop("disabled")
        console.log(isDisabled)
        if (isDisabled) {
            console.log('isDisabled')
            event.preventDefault(); // Don't submit yet, build JSON first
        } else {
    
        }
    });
    
    $("#userundergradbutton").click(function(){
        
        event.preventDefault();
        
        console.log('under pushpush')
        
        var isDisabled = $("#userundergradbutton").prop('disabled')
        console.log(isDisabled)
        if (isDisabled) {
            console.log('isDisabled')
            event.preventDefault(); // Don't submit yet, build JSON first
        } else {
    
        }
    });
    
    $("#userfifthbutton").click(function(){
        
        event.preventDefault();
        
        console.log('fifth pushpush')
        
        var isDisabled = $("#userfifthbutton").prop('disabled')
        console.log(isDisabled)
        if (isDisabled) {
            console.log('isDisabled')
            event.preventDefault(); // Don't submit yet, build JSON first
        } else {
    
        }
    });
    
    
    $("#bacbutton").click(function(){
        
        event.preventDefault(); // Don't submit yet, build JSON first
        var data = {};
        
        var date = $("#post-bac").val();
        
        data["date"] = date
        data["button"] = 'post-bac'
        
        console.log('yass')
        $('#bacbutton').prop('disabled', true);
        
        $.ajax({
            url:"/admin/updateDeadline",
            type:"POST",
            data:JSON.stringify(data),
            contentType:"application/json; charset=utf-8",
            dataType:"json",
            success: function(result) {
                console.log(result);
                $("#bac_yes").show();
                setTimeout(function() { $("#bac_yes").hide(); }, 3000);
            }
        });
        
        
    });
    
    $("#undergradbutton").click(function(){
        event.preventDefault(); // Don't submit yet, build JSON first
        var data = {};
        
        var date = $("#Undergrad").val();
        
        data["date"] = date
        data["button"] = 'Undergrad'
        
        console.log('yass')
        $('#undergradbutton').prop('disabled', true);
        
        $.ajax({
            url:"/admin/updateDeadline",
            type:"POST",
            data:JSON.stringify(data),
            contentType:"application/json; charset=utf-8",
            dataType:"json",
            success: function(result) {
                console.log(result);
                $("#undergrad_yes").show();
                setTimeout(function() { $("#undergrad_yes").hide(); }, 3000);
            }
        });
    }); 
    
    $("#fifthbutton").click(function(){
        event.preventDefault(); // Don't submit yet, build JSON first
        var data = {};
        
        var date = $("#FifthYear").val();
        
        data["date"] = date
        data["button"] = 'FifthYesar'
        
        console.log('yass')
        $('#fifthbutton').prop('disabled', true);
        
        $.ajax({
            url:"/admin/updateDeadline",
            type:"POST",
            data:JSON.stringify(data),
            contentType:"application/json; charset=utf-8",
            dataType:"json",
            success: function(result) {
                console.log(result);
                $("#fifth_yes").show();
                setTimeout(function() { $("#fifth_yes").hide(); }, 3000);
            }
        });
    }); 
    
    $('#post-bac').change(function() {
        var date = $("#post-bac").val();
        console.log(date, 'change');
        $('#bacbutton').prop('disabled', false);
    });
    
    $('#Undergrad').change(function() {
        var date = $("#undergrad").val();
        console.log(date, 'change');
        $('#undergradbutton').prop('disabled', false);
    });
    
    $('#FifthYear').change(function() {
        var date = $("#FifthYear").val();
        console.log(date, 'change');
        $('#fifthbutton').prop('disabled', false);
    });
    
    
    $("#bacbutton").click(function() {
        console.log( "Handler for .bac called." );
    });
    
    // If an endorsementArea exists, add its data
    if ($('table#endorsementArea').length) { 
        buildEndorsementArea(); 
    }
    
    // If practicum table exists, add its data
    if ($('table#practicum').length) {
        buildPracticum();   
    }
    
    // If relationships table exists, add its data
    if ($('table#relationships').length) {
        buildRelationships();   
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

$(document).on('click', 'button.delRow', function() {
    // Check if this is the last remaining row, and if not, delete row
    if ($(this).closest("tbody").find("tr").length <= 1) { 
        alert("Can't remove the last remaining row."); 
    }
    else {
        let thisRow = $(this).closest("tr");
        delRow(thisRow);
    }
});

$(document).on('click', 'button.addRow', function() {
    let tbody = $(this).prev("table").find("tbody")[0];
    addRow(tbody);
});
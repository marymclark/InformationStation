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
    
}

function buildPracticum() {
    // Add elements
    $("#practicum tbody").append('<tr><td><select class="form-control" name="district" id="district"></td></tr>');
    $("#practicum tbody tr").append('<td><select class="form-control" name="school" id="school"></select></td>');
    $("#practicum tbody tr").append('<td><select class="form-control" name="grades" id="grades"></select></td>');
    $("#practicum tbody tr").append('<td><select class="form-control" name="subjects" id="subjects"></select></td>');
    $("#practicum tbody tr").append('<td><button type="button" class="btn delRow"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td>');
    
    $.getJSON("/data/schools", function(data) {
        data = data['data'];
        let first_level = [];
        for (var key in data) {
            first_level.push(data[key].district);
        }
        
        // Add first level
        for (var key in first_level) {
            $("#district").append('<option value="'+key+'">'+first_level[key]+'</option>');
        }
        
        $("#district").change(function() {
            let index1 = $("#district").val();
            let selection = data[index1]; 
            $("#school").empty();
            $("#grades").empty();
            
            if (selection.schools != undefined) { // If schools exist
                // Build second_level
                let second_level = [];
                for (var key in selection.schools) {
                    second_level.push(selection.schools[key].school);
                }
                
                // Empty and add new elements
                for (var key in second_level) {
                    $("#school").append('<option value="'+key+'">'+second_level[key]+'</option>');
                }
                
                // Listen for changes in the second district
                $("#school").change(function() {
                    $("#grades").empty();
                    let index2 = $("#school").val();
                    let third_level;
                    let selection = data[index1].schools[index2]; 
                    console.log(index1 + " " + index2);
                    console.log(selection);
                    
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
                        $("#grades").append('<option value="'+key+'">'+third_level[key]+'</option>');
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
    
    $("#bacbutton").click(function(){
        console.log('yass')
        $('#bacbutton').prop('disabled', true);
        
        var date = $("#postbac").val();
        
        $.ajax({
            url:"/updateDeadline",
            type:"POST",
            data:JSON.stringify(date),
            contentType:"application/json; charset=utf-8",
            dataType:"json",
            success: function(result) {
                console.log(result);
            }
    });
        
    });
    
    $("#undergradbutton").click(function(){
        console.log('yass')
        $('#undergradbutton').prop('disabled', true);
    }); 
    
    $("#fifthbutton").click(function(){
        console.log('yass')
        $('#fifthbutton').prop('disabled', true);
    }); 
    
    $('#postbac').change(function() {
        var date = $("#postbac").val();
        console.log(date, 'change');
        $('#bacbutton').prop('disabled', false);
    });
    
    $('#undergrad').change(function() {
        var date = $("#postbac").val();
        console.log(date, 'change');
        $('#undergradbutton').prop('disabled', false);
    });
    
    $('#fifthyear').change(function() {
        var date = $("#postbac").val();
        console.log(date, 'change');
        $('#fifthbutton').prop('disabled', false);
    });
    
    
    $("#bacbutton").click(function() {
        console.log( "Handler for .bac called." );
    });
    
    //$('#userTable').DataTable();
    $('#exportFormTable').DataTable();
    $('#deleteFormTable').DataTable();
    
    // Array holding selected row IDs
   var rows_selected = [];
   var table = $('#userTable').DataTable({
 
      "processing": true,
      "serverSide": true,
      "ajax": "{{ url_for('admin.userTable') }}",
      
      'columnDefs': [{
         'targets': 0,
         'searchable': false,
         'orderable': false,
         'width': '1%',
         'className': 'dt-body-center',
         'render': function (data, type, full, meta){
             return '<input type="checkbox">';
         }
      }],
      'order': [[1, 'asc']],
      'rowCallback': function(row, data, dataIndex){
         // Get row ID
         var rowId = data[0];

         // If row ID is in the list of selected row IDs
         if($.inArray(rowId, rows_selected) !== -1){
            $(row).find('input[type="checkbox"]').prop('checked', true);
            $(row).addClass('selected');
         }
      }
   });

   // Handle click on checkbox
   $('#userTable tbody').on('click', 'input[type="checkbox"]', function(e){
      var $row = $(this).closest('tr');

      // Get row data
      var data = table.row($row).data();

      // Get row ID
      var rowId = data[0];

      // Determine whether row ID is in the list of selected row IDs 
      var index = $.inArray(rowId, rows_selected);

      // If checkbox is checked and row ID is not in list of selected row IDs
      if(this.checked && index === -1){
         rows_selected.push(rowId);

      // Otherwise, if checkbox is not checked and row ID is in list of selected row IDs
      } else if (!this.checked && index !== -1){
         rows_selected.splice(index, 1);
      }

      if(this.checked){
         $row.addClass('selected');
      } else {
         $row.removeClass('selected');
      }

      // Update state of "Select all" control
      updateDataTableSelectAllCtrl(table);

      // Prevent click event from propagating to parent
      e.stopPropagation();
   });

   // Handle click on table cells with checkboxes
   $('#userTable').on('click', 'tbody td, thead th:first-child', function(e){
      $(this).parent().find('input[type="checkbox"]').trigger('click');
   });

   // Handle click on "Select all" control
   $('thead input[name="select_all"]', table.table().container()).on('click', function(e){
      if(this.checked){
         $('#userTable tbody input[type="checkbox"]:not(:checked)').trigger('click');
      } else {
         $('#userTable tbody input[type="checkbox"]:checked').trigger('click');
      }

      // Prevent click event from propagating to parent
      e.stopPropagation();
   });

   // Handle table draw event
   table.on('draw', function(){
      // Update state of "Select all" control
      updateDataTableSelectAllCtrl(table);
   });

   // Handle delete
   $('#deleteUser').click(function(){
       
       console.log('deleting user')
       
           $('input:checked').each(function(){
               $("table tr input:checked").parents('tr').remove();
               console.log('deleting user!')
           });
   });
    
    // $(document) instead $(document) necessary...?
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
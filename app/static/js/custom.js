// Form Functions

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
        $("#endorsementArea tbody tr").append('<td><button type="button" class="btn delRow"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td>');
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
    
    //$('#userTable').DataTable();
    $('#exportFormTable').DataTable();
    $('#deleteFormTable').DataTable();
    
    // Array holding selected row IDs
   var rows_selected = [];
   var table = $('#userTable').DataTable({
      //'ajax': {
    //     'url': '/lab/articles/jquery-datatables-checkboxes/ids-arrays.txt' 
      //},
       "data": [
          [
             "1",
             "Tiger Nixon",
             "System Architect",
             "Edinburgh",
             "5421",
             "2011/04/25",
             "$320,800"
          ]],
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

   // Handle form submission event 
   $('#frm-example').on('submit', function(e){
      var form = this;
      
      // Iterate over all selected checkboxes
      $.each(rows_selected, function(index, rowId){
         // Create a hidden element 
         $(form).append(
             $('<input>')
                .attr('type', 'hidden')
                .attr('name', 'id[]')
                .val(rowId)
         );
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
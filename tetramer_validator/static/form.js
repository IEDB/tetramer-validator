var num_rows = 0;
$(document).ready(function() {
  $('[data-toggle="popover"]').popover({
    html: true
  });
  newMHCTypeahead();
  newPTMTypeahead("#".concat(num_rows.toString()));
});

function addButton() {
  var string = "#0";
  console.log("x");
  $(".mhc_name input").typeahead('destroy');
  var tokens_zero = $("#0 .mod_type input").tokenfield('getTokens');
  $("#0 .mod_type input").tokenfield('destroy');
  var x = $(string).clone(true, true);
  x.find("input").val('')
  num_rows = num_rows + 1;
  //x.removeAttr("id");
  $(x).attr("id", num_rows.toString());
  num_rows = num_rows-1;
  $(x).insertAfter("#".concat(num_rows.toString()));
  num_rows += 1;
  newMHCTypeahead();
  newPTMTypeahead("#".concat(num_rows.toString()));
  newPTMTypeahead("#0");
  console.log(tokens_zero);
  $("#0 .mod_type input").tokenfield('setTokens', tokens_zero);
}

$("#Add").click(function(event) {
  addButton();
  event.stopPropagation();
});

$("#Clear").click(function(event) {
  $("input").val("");
  $("input").removeClass("is-valid");
  $("input").removeClass("is-invalid");
  event.preventDefault();
});

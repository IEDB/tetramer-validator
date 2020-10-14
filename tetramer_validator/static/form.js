var num_rows = 0;
$(document).ready(function() {
  $('[data-toggle="popover"]').popover({
    html: true
  });
  newMHCTypeahead();
  newPTMTypeahead("#0");
});
$("#Add").click(function(event) {
  var string = "#0";
  $(".mhc_name input").typeahead('destroy');
  var tokens_zero = $("#0 .mod_type input").tokenfield('getTokens');
  $("#0 .mod_type input").tokenfield('destroy');
  var x = $(string).clone(true, true);
  x.find("input").val('')
  num_rows = num_rows + 1;
  $(x).find("input").removeClass('is-invalid');
  $(x).find("input").removeClass('is-valid');
  //x.removeAttr("id");
  $(x).attr("id", num_rows.toString());
  num_rows = num_rows-1;
  $(x).insertAfter(".".concat(num_rows.toString()));
  num_rows += 1;
  if(!($(".post-action").hasClass(num_rows.toString()))) {
     $("<div class = 'post-action ".concat(num_rows.toString(), "' </div>")).insertAfter($(".form-row").last());
  }
  newMHCTypeahead();
  newPTMTypeahead("#".concat(num_rows.toString()));
  newPTMTypeahead("#0");
  $("#0 .mod_type input").tokenfield('setTokens', tokens_zero);
  event.preventDefault();
  //event.stopPropagation();
  //return false;
});

$("#Clear").click(function(event) {
  $("input").val("");
  $("input").removeClass("is-valid");
  $("input").removeClass("is-invalid");
  event.preventDefault();
});

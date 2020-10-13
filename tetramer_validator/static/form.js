var num_rows = 0;
$(document).ready(function() {
  $('[data-toggle="popover"]').popover({
    html: true
  });
  newMHCTypeahead();
  newPTMTypeahead();
});


$("#Add").click(function(event) {
  var string = "#1";
  $(".mhc_name input").typeahead('destroy');
  $(".mod_type input").tokenfield('destroy');
  var x = $(string).clone(true, true);

  num_rows = num_rows + 1;
  //x.removeAttr("id");
  $(x).attr("id", num_rows.toString());
  num_rows = num_rows-1;
  $(x).insertAfter("#".concat(num_rows.toString()));
  num_rows += 1;
  newMHCTypeahead();
  newPTMTypeahead();
  event.preventDefault();
});


$("#Clear").click(function(event) {
  $("input").val("");
  $("input").removeClass("is-valid");
  $("input").removeClass("is-invalid");
  event.preventDefault();
});

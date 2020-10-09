// $(document).ready(function(){
//   $('[data-toggle="popover"]').popover({html: true});
// });

function removePlaceholders() {
  $("input").removeAttr("placeholder");
}

function field_error_highlight(field) {
var field = field;
$(field).addClass("is-invalid");
}

function field_success_highlight() {
  $("input").removeClass("is-invalid");
  var inputs = $("input[id]");
  for(input = 0; input < inputs.length; input++) {
    if(inputs[input].value != "") {
      $(inputs[input]).addClass("is-valid");
    }
  }
  removePlaceholders();
}

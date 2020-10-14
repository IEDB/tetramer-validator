function removePlaceholders(selector) {
  $(selector).removeAttr("placeholder");
}

function field_error_highlight(field) {
  var field = field;
  $(field).addClass("is-invalid");
}

function field_success_highlight(num_row) {
  var selector = num_row.concat(" input");
  $(selector).removeClass("is-invalid");
  var inputs = $(selector);
  for (input = 0; input < inputs.length; input++) {
    console.log(inputs[input].name);
    console.log(inputs[input].value);
    if (inputs[input].value != "") {
      $(inputs[input]).addClass("is-valid");
    }
  }
  removePlaceholders(selector);
}

$("form").submit(function(event) {
  console.log($(this).serializeArray());
  //event.preventDefault();
});

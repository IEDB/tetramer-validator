$(document).ready(function(){
  $(".mod_type.is-invalid").parent().addClass("is-invalid");
  $(".mod_type.is-valid").parent().addClass("is-valid");
});
$('svg').focus(function(event) {
  $('[data-toggle="popover"]').popover({html: true});
  event.preventDefault();
});

$(document).ready(function(){
  $(".mod_type.is-invalid").parent().addClass("is-invalid");
  $(".mod_type.is-valid").parent().addClass("is-valid");
});
$('.bi-question').focus(function(event) {
  $('[data-toggle="popover"]').popover({html: true});
});
$('.bi-trash-fill').click(function(event) {
  if ($(".entry").length == 1) {
    window.location.href = "/";
  }
  else {
    $(this).closest('.entry').remove();
    event.preventDefault();
  }
});

$(document).ready(function(){
  $(".mod_type.is-invalid").parent().addClass("is-invalid");
  $(".mod_type.is-valid").parent().addClass("is-valid");
  $(function () {
    $('[data-toggle="popover"]').popover({trigger: "click", html: true})
  });
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

$("#Copy").click(function(){
    $("#Output").select();
    document.execCommand('copy');
});

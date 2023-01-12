$(function() {
  $('#edit').click(function(){
    $('#orig_txt').slideToggle();
  });
});

$('#upload .fileinput').on('change', function () {
 var file = $(this).prop('files')[0];
 $(this).closest('#upload').find('#filename').text(file.name);
});

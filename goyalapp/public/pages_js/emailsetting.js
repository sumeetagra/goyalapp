$(function(){
    $('.select2').select2();
  $('.mainsmtpDIV').hide();
  var set_email_engine = $("#email_engine").val();;
  if(set_email_engine == 'smtp') {
      $(".mainsmtpDIV").show('slow');
  } else if(set_email_engine == 'sendmail') {
      $(".mainsmtpDIV").hide('slow');
  } else if(set_email_engine == 'select') {
      $('.mainsmtpDIV').hide();
  } else {
     if(set_email_engine == 'smtp')
          $('.mainsmtpDIV').show();
  }

  $(document).on('change', "#email_engine", function() {
     "use strict";
      var get_email_engine = $(this).val();
      if(get_email_engine == 'smtp') {
          $(".mainsmtpDIV").show('slow');
      } else {
          $(".mainsmtpDIV").hide('slow');
      }
  });
});


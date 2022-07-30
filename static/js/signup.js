$(function() {

  $("#signupForm input,#signupForm select").jqBootstrapValidation({
    preventSubmit: true,
    submitError: function($form, event, errors) {
      // additional error messages or events
    },
    submitSuccess: function($form, event) {
      event.preventDefault(); // prevent default submit behaviour
      // get values from FORM
      var email = $("input#email").val();
      var subreddits = $("select#subreddits").val();
      var captcha_token = $("input#captcha_input").val();
      var email_interval = $('input[name=email_interval]:checked').val();
      if (subreddits.length > 10) {
        alert('Too many subreddits selected, maximum is 10.');
        return;
      }
      $this = $("#sendMessageButton");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
      $.ajax({
        url: "/signup",
        type: "POST",
        data: {
          email: email,
          subreddits: subreddits,
          captcha_token: captcha_token,
          email_interval: email_interval
        },
        cache: false,
        success: function() {
          // Success message
          $('#success').html("<div class='alert alert-success'>");
          $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success > .alert-success')
            .append("<strong>Success! You should receive your first email soon.<br>To ensure you receive your email, please add no-reply@orangered.email to your contacts.</strong>");
          $('#success > .alert-success')
            .append('</div>');
          // clear all fields
          $('#signupForm').trigger("reset");
          $('select').val('').trigger('chosen:updated');
        },
        error: function(resp, t, e) {
          var text = resp.status === 400 ? "Error: " + resp.responseText : "An error occurred. Please try again later!";
          $('#success').html("<div class='alert alert-danger'>");
          $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success > .alert-danger').append($("<strong>").text(text));
          $('#success > .alert-danger').append('</div>');
        },
        complete: function() {
          setTimeout(function() {
            $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
          }, 1000);
          // reset captcha
          if (window.recaptchaSiteKey) {
              grecaptcha.execute(recaptchaSiteKey, {action: 'homepage'}).then(function(token) {
                $('#captcha_input').val(token);
              });
          }
        }
      });
    },
    filter: function() {
      return $(this).is(":visible");
    },
  });

  $("a[data-toggle=\"tab\"]").click(function(e) {
    e.preventDefault();
    $(this).tab("show");
  });
});

/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
  $('#success').html('');
});

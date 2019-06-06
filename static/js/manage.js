$(function() {

  $("#manageForm select").jqBootstrapValidation({
    preventSubmit: true,
    submitError: function($form, event, errors) {
      // additional error messages or events
    },
    submitSuccess: function($form, event) {
      event.preventDefault(); // prevent default submit behaviour
      // get values from FORM
      var subreddits = $("select#subreddits").val();
      if (subreddits.length > 10) {
        alert('Too many subreddits selected, maximum is 10.');
        return;
      }
      var email_interval = $('input[name=email_interval]:checked').val();
      $this = $("#manageButton");
      $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
      $.ajax({
        url: document.location.pathname,
        type: "POST",
        data: {
          subreddits: subreddits,
          email_interval: email_interval
        },
        cache: false,
        success: function() {
          // Success message
          $('#success').html("<div class='alert alert-success'>");
          $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
            .append("</button>");
          $('#success > .alert-success')
            .append("<strong>Success! Subreddits updated.</strong>");
          $('#success > .alert-success')
            .append('</div>');
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

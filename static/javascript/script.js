const emailPattern = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;

function emailError(error) {
  if (!error) {
    $("#user-email").removeClass("valid taken");
    $("#email_err").hide();
    $("#user-email").css("border", "1px solid #34F458");
  } else {
    $("#email_err").text(error);
    $("#email_err").show();
    $("#user-email").css("border", "1px solid #F90A0A");
  }
}

$("#user-email").blur(function () {
  const email = $(this).val();

  if (email === "") {
    emailError("Email cannot be blank");
    return;
  }

  if (!emailPattern.test(email)) {
    emailError("Invalid email address");
    return;
  }
  var token = $("input[name = csrfmiddlewaretoken]").val();
  $.ajax({
    data: { email, csrfmiddlewaretoken: token },
    url: "/validate-email",
    method: "POST",

    success: function (response) {
      if (response.is_taken) {
        $("#user-email").addClass("taken");
        emailError("Email address already exists! Use another one or log in");
      } else {
        // $("#user-email").addClass("valid");
        emailError(null);
      }
    },
    error: function (response) {
      console.log(response.errors);
    },
  });
});

const usernamePattern = /^[a-zA-Z0-9]+$/;
function userNameError(error) {
  if (!error) {
    $("#user-name").removeClass("valid taken");
    $("#username_err").hide();
    $("#user-name").css("border", "1px solid #34F458");
  } else {
    $("#username_err").text(error);
    $("#username_err").show();
    $("user-name").css("border", "1px solid #F90A0A");
  }
}

$("#user-name").blur(function () {
  const username = $(this).val();

  if (username === "") {
    userNameError("User Name cannot be blank");
    return;
  }

  if (!usernamePattern.test(username)) {
    userNameError("Invalid User Name");
    return;
  }
  var token = $("input[name = csrfmiddlewaretoken]").val();
  $.ajax({
    data: { username, csrfmiddlewaretoken: token },
    url: "/validate-username",
    method: "POST",

    success: function (response) {
      if (response.is_taken) {
        $("#user-name").addClass("taken");
        userNameError("User Name already exists! Use another one or log in");
      } else {
        // $("#user-name").addClass("valid");
        userNameError(null);
      }
    },
    error: function (response) {
      console.log(response.errors);
    },
  });
});

const phoneNumberPattern =
  /^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/;

function phoneError(error) {
  if (!error) {
    $("#user-phone_1").removeClass("valid taken");
    $("#phone_err").hide();
    $("#user-phone_1").css("border", "1px solid #34F458");
  } else {
    $("#phone_err").text(error);
    $("#phone_err").show();
    $("user-phone_1").css("border", "1px solid #F90A0A");
  }
}

$("#user-phone_1").blur(function () {
  var number = $(this).val();
  if (number === "") {
    phoneError("Phone Number cannot be blank");
    return;
  } else if (!phoneNumberPattern.test(number)) {
    phoneError("Invalid Phone Number");
    return;
  } else if (number < 10) {
    phoneError("Invalid Phone Number");
    return;
  } else {
    phoneError(null);
  }
});

const firstNamePattern =/^[a-z ,.'-]+$/i;

function fistNameError(error) {
  if (!error) {
    $("#first_name_input").removeClass("valid taken");
    $("#name_err").hide();
    $("#first_name_input").css("border", "1px solid #34F458");
  } else {
    $("#name_err").text(error);
    $("#name_err").show();
    $("first_name_input").css("border", "1px solid #F90A0A");
  }
}

$("#first_name_input").blur(function () {
  var name = $(this).val();
  if (name === "") {
    fistNameError("First Name cannot be blank");
    return;
  } else if (!firstNamePattern.test(name)) {
    fistNameError("Invalid First Name");
    return;
  } else {
    fistNameError(null);
  }
});

// ADMIN USER APPROVAL REQUESTS
function rejectUser(userId) {
  swal({
    title: "Are you sure?",
    text: "Once Rejected, registration details will be erased!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/reject-request/0".replace(
        "0",
        parseInt(userId)
      );
    } else {
      swal("Operation Aborted!");
    }
  });
}

function approveUser(userId) {
  swal({
    title: "Are you sure?",
    text: "Approval Request will be accepted and login credentials will be send!",
    icon: "info",
    buttons: true,
    dangerMode: true,
  }).then((willApprove) => {
    if (willApprove) {
      window.location.href = "/approve-request/0".replace(
        "0",
        parseInt(userId)
      );
    } else {
      swal("Operation Aborted!");
    }
  });
}
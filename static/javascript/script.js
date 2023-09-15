// Profile
$("#update-image-btn").click(() => {
  $("#image-input-seg").css("display", "block");
  $("#update-image-btn").css("display", "none");
});
$("#image-input-cancel").click(() => {
  $("#image-input-seg").css("display", "none");
  $("#update-image-btn").css("display", "block");
});

function removeProfileImage() {
  swal({
    title: "Are you sure?",
    text: "Profile Image will be removed!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/remove-profile-image";
    } else {
      swal("Operation Aborted!");
    }
  });
}

$(document).ready(function () {
  $(".wish-icon i").click(function () {
    $(this).toggleClass("fa-heart fa-heart-o");
  });
});

// ADD TO CART

function addToCart(bookId) {
  var bookId = parseInt(bookId);
  var token = $("input[name = csrfmiddlewaretoken]").val();
  $.ajax({
    method: "POST",
    url: "/add-to-cart",
    data: {
      book: bookId,
      csrfmiddlewaretoken: token,
    },
    success: (response) => {
      // alert(response.cartCount);
      $("#cart-count").html(response.cartCount);
      $("#buy" + bookId).html(`<i class="fa fa-check me-2"></i>In Cart`);
      if (response.stock == 0) {
        $("#buy" + bookId).prop("disabled", true);
      } else {
        $("#buy" + bookId).prop("disabled", false);
      }
    },
  });
}

function buyNow(bookId) {
  var bookId = parseInt(bookId);
  var token = $("input[name = csrfmiddlewaretoken]").val();
  $.ajax({
    method: "POST",
    url: "/add-to-cart",
    data: {
      book: bookId,
      csrfmiddlewaretoken: token,
    },
    success: (response) => {
      // alert(response.cartCount);
      $("#cart-count").html(response.cartCount);
      window.location.href = "/cart";
    },
  });
}

// Remove cart Item
function removeCartItem(bookId) {
  swal({
    title: "Are you sure?",
    text: "Once deleted, item will be removed from the cart!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/remove-cart-item/0".replace(
        "0",
        parseInt(bookId)
      );
    } else {
      swal("Operation Aborted!");
    }
  });
}

function changeQuantity(cartId, prodId, count) {
  var incCount = count;
  var display = parseInt(cartId);
  //   let quantity = $("#" + display).val();
  let quantity = document.getElementById("qnt" + display).innerHTML;
  var token = $("input[name = csrfmiddlewaretoken]").val();
  $.ajax({
    method: "POST",
    url: "/change-product-quantity",
    data: {
      cart: cartId,
      book: prodId,
      count: incCount,
      quantity: quantity,
      csrfmiddlewaretoken: token,
    },
    success: (response) => {
      $("#qnt" + display).html(response.qty);
      $("#price" + display).html(response.totPrice);
      $("#cart-total").html(response.sum);
      $("#sum-total").html(response.sum);
      if (response.qty == 1) {
        $("#dec-btn" + display).prop("disabled", true);
      } else {
        $("#dec-btn" + display).prop("disabled", false);
      }
      if (response.stock == 0) {
        $("#inc-btn" + display).prop("disabled", true);
        $("#stock" + display).css("display", "block");
        $("#stock-no" + display).text(response.qty);
        $("#stock1" + display).css("display", "none");
      } else {
        $("#inc-btn" + display).prop("disabled", false);
        $("#stock" + display).css("display", "none");
      }
    },
  });
}

// Rental Operations

function addDays(date, days) {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}
$("#rental-period").keyup(() => {
  var days = parseInt($("#rental-period").val());
  if (days < 1 || days > 30 || isNaN(days)) {
    $("#days-invalid").css("display", "block");
    $("#rentamount").css("display", "none");
    $(".due-date-seg").css("display", "none");
  } else {
    $("#days-invalid").css("display", "none");
    cDate = new Date().toLocaleDateString();
    var dueDate = addDays(cDate, days).toLocaleDateString();

    $(".due-date-seg").css("display", "block");
    $("#duedate").text(dueDate);
    // var netAmount = $("#rent-price").val();
    var amount = document.getElementById("rent-price").innerHTML;
    var netAmount = parseInt(amount) * days;
    $("#rent-amount").text(netAmount);
    $("#rentamount").css("display", "block");
    $("#subtotal").text(netAmount);
    $("#netamount").text(netAmount + 10);
    // document.getElementById("rentamountInput").value = netAmount+10;
    // document.getElementById("duedateInput").value = `dueDate`;
  }
});

function rentOut(bookId) {
  var bookId = parseInt(bookId);
  var days = parseInt($("#rental-period").val());
  var token = $("input[name = csrfmiddlewaretoken]").val();
  var dueDate = document.getElementById("duedate").innerHTML;
  var rentAmount = document.getElementById("rent-amount").innerHTML;
  var payment = $("input[type='radio'][name='PaymentMethod']:checked").val();
  if (payment == undefined) {
    swal({
      position: "top-end",
      icon: "warning",
      title: "Please choose a Payment Method",
    });
  } else {
    $.ajax({
      method: "POST",
      url: "/checkout-rental",
      data: {
        book: bookId,
        dueDate: dueDate,
        days: days,
        payment: payment,
        amount: rentAmount,
        csrfmiddlewaretoken: token,
      },
      success: (response) => {
        window.location.href = "/rental-request-placed";
        // alert('success')
      },
    });
  }
}

window.onload = () => {
  var sum = parseFloat(document.getElementById("subtotal").innerHTML);
  var netSum = sum + 20.0;
  $("#netamount").html(netSum);
  document.getElementById("netamountInput").value = netSum;
};

//SignUp validations

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

function resetPassword() {
  var token = $("input[name = csrfmiddlewaretoken]").val();
  var currentPassword = $("#currentPassword").val();
  var newPassword = $("#newPassword").val();
  var confirmPassword = $("#confirmPassword").val();
  $.ajax({
    data: {
      currentPassword,
      newPassword,
      confirmPassword,
      csrfmiddlewaretoken: token,
    },
    url: "/reset-password",
    method: "POST",

    success: function (response) {
      if (response.status) {
        swal({
          position: "top-end",
          icon: "success",
          title: "Password updated successfully. Please login again.",
        }).then(function () {
          window.location = "/user-logout";
        });
        // $("#resetPassword").removeClass('show');
        $("#currentPassword").val("");
        $("#newPassword").val("");
        $("#confirmPassword").val("");
        $("#resetPassword").modal("toggle");
        // window.location.href="/sign-in"
      } else {
        swal({
          position: "top-end",
          icon: "error",
          title: response.message,
        });
      }
    },
    error: function (response) {
      swal({
        position: "top-end",
        icon: "error",
        title: response.errors,
      });
    },
  });
}

const passwordPattern =
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$/;

function passwordError(error) {
  if (!error) {
    $("#newPassword").removeClass("valid taken");
    $("#password_err").hide();
    $("#newPassword").css("border", "1px solid #34F458");
  } else {
    $("#password_err").text(error);
    $("#password_err").show();
    $("newPassword").css("border", "1px solid #F90A0A");
  }
}
$("#newPassword").blur(function () {
  var newpassword = $(this).val();
  var password = newpassword.replace(/\s/g, "");
  $("#newPassword").val(password);
  $("#confirmPassword").val("");
  if (password === "") {
    passwordError("Password cannot be blank");
    $("#resetbtn").prop("disabled", true);
    return;
  } else if (!passwordPattern.test(password)) {
    passwordError(
      "Password should contain 8-15 characters with at least one uppercase ,lower case, number and special character. "
    );
    $("#resetbtn").prop("disabled", true);
    return;
  } else {
    $("#resetbtn").prop("disabled", false);
    passwordError(null);
  }
});

// Confirm password
$("#confirmPassword").blur(function () {
  var pass1 = $("#newPassword").val();
  var pass2 = $("#confirmPassword").val();
  if (pass1 != "" && pass1 != pass2) {
    $("#confirmPass_err").text("Passwords doesn't match..Please try again.");
    $("#resetbtn").prop("disabled", true);
  } else {
    $("#confirmPass_err").text("");
    $("#resetbtn").prop("disabled", false);
  }
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

const firstNamePattern = /^[a-z ,.'-]+$/i;

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

function confirmPassword() {
  var pass1 = document.getElementById("newPassword").value;
  var pass2 = document.getElementById("confirmPassword").value;
  var div = document.getElementById("confirmPassword_err");
  if (pass1 != "") {
    if (pass1 != pass2) {
      div.innerHTML = "Passwords doesn't match..Please try again.";
    } else {
      div.innerHTML = "";
    }
  }
}

// $('#add-new-adrs').click(()=>{
//   if($('#address-form-seg').css('display') == 'none'){
//     $('#address-form-seg').css('display') == 'block'
//   }
//   else if($('#address-form-seg').css('display') == 'block'){
//     $('#address-form-seg').css('display') == 'none'
//   }
// })

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
      window.location.href = "/reject-request/0".replace("0", parseInt(userId));
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

// Remove Book
function removeBook(bookId) {
  swal({
    title: "Are you sure?",
    text: "Once Removed, Book details will be erased permanently!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/remove-book/0".replace("0", parseInt(bookId));
    } else {
      swal("Operation Aborted!");
    }
  });
}

// Remove Category
function removeCategory(categoryId) {
  swal({
    title: "Are you sure?",
    text: "Once Removed, Books in the particular category also will be disappears!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/remove-category/0".replace(
        "0",
        parseInt(categoryId)
      );
    } else {
      swal("Operation Aborted!");
    }
  });
}

// Remove Publisher
function removePublisher(publisherId) {
  swal({
    title: "Are you sure?",
    text: "Once Removed, Books associated with the particular publisher also may be disappeared!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/remove-publisher/0".replace(
        "0",
        parseInt(publisherId)
      );
    } else {
      swal("Operation Aborted!");
    }
  });
}

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
      swal({ icon: "success", text: "Operation Aborted!" });
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
      swal({ icon: "success", text: "Operation Aborted!" });
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
function diffInDays(dueDate) {
  const cDate = new Date().toLocaleDateString();
  const dDate = new Date(dueDate);
  const diffTime = Math.abs(cDate - dDate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  alert(diffDays);
}

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
// LOST PENALTY
// function getPenaltyAmount(price,id){
//   var bookPrice = parseFloat(price);
//   var penaltyAmount = bookPrice + (bookPrice*0.03);
//   $("#penalty-amount").text(penaltyAmount);
//   $("#lost-confirm").attr('onClick','confirmLost()')
// }
function passDueAmount(dueAmount, rentalId) {
  var amount = parseFloat(dueAmount);
  $("#pay-due-amount-value").text(dueAmount);
  $("#due-rental-id").val(rentalId);
}

function passPenaltyAmount(dueAmount, rentalId) {
  var amount = parseFloat(dueAmount);
  $("#pay-penalty-amount-value").text(dueAmount);
  $("#pay-penalty-amount-button").text(dueAmount);
  $("#penalty-rental-id").val(rentalId);
}

function payReturn() {
  var id = $("#due-rental-id").val();
  alert(id);
}

function confirmLostBook(bookId, price, rentalId) {
  var bookPrice = parseFloat(price);
  var penaltyAmount = bookPrice + bookPrice * 0.03;

  swal({
    title: "Are you sure?",
    text:
      "You are required to pay a penalty of Rs. " +
      penaltyAmount +
      " (Book's price + 3% additional charge), as per the T&C of Rental agreements. Please confirm.!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/report-lost-book/0/1"
        .replace("0", parseInt(bookId))
        .replace("1", parseInt(rentalId));
    } else {
      swal({ icon: "success", text: "Operation Aborted!" });
    }
  });
}

// Return Book
function returnBook(rentalId) {
  swal({
    title: "Are you sure?",
    text: "Are You sure you want to return the book.?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/user-return-book/0".replace(
        "0",
        parseInt(rentalId)
      );
    } else {
      swal({ icon: "success", text: "Operation Aborted!" });
    }
  });
}

window.onload = () => {
  var sum = parseFloat(document.getElementById("subtotal").innerHTML);
  var netSum = sum + 20.0;
  $("#netamount").html(netSum);
  document.getElementById("netamountInput").value = netSum;
};

// ISBN Validation
const isbnPattern = /^(\d{13})?$/;
function isbnError(error) {
  if (!error) {
    $("#isbnInput").removeClass("valid taken");
    $("#isbn_err").hide();
    $("#isbnInput").css("border", "1px solid #34F458");
  } else {
    $("#isbn_err").text(error);
    $("#isbn_err").show();
    $("#isbnInput").css("border", "1px solid #F90A0A");
  }
}

$("#isbnInput").blur(function () {
  const isbn = $(this).val();

  if (isbn === "") {
    isbnError("ISBN cannot be blank");
    return;
  }

  if (!isbnPattern.test(isbn)) {
    isbnError("Invalid ISBN, It should be a 13 digit unique number");
    return;
  } else {
    isbnError(null);
  }
  var token = $("input[name = csrfmiddlewaretoken]").val();
  $.ajax({
    data: { isbn, csrfmiddlewaretoken: token },
    url: "/validate-isbn",
    method: "POST",

    success: function (response) {
      if (response.is_taken) {
        $("#user-email").addClass("taken");
        isbnError("ISBN already exists!, number should be unique.");
      } else {
        // $("#user-email").addClass("valid");
        isbnError(null);
      }
    },
    error: function (response) {
      console.log(response.errors);
    },
  });
});

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

//Address validation => basic validation with regular expression
// house-flat streetAddress city state country zip
const zipPattern = /^\d{5,9}$/;
const stateCountryPattern = /^[a-zA-Z]{2,}$/;

function zipError(error) {
  if (!error) {
    $("#zip").removeClass("valid taken");
    $("#zip_err").hide();
    $("#zip").css("border", "1px solid #34F458");
  } else {
    $("#zip_err").text(error);
    $("#zip_err").show();
    $("zip").css("border", "1px solid #F90A0A");
  }
}
function stateError(error) {
  if (!error) {
    $("#state").removeClass("valid taken");
    $("#state_err").hide();
    $("#state").css("border", "1px solid #34F458");
  } else {
    $("#state_err").text(error);
    $("#state_err").show();
    $("state").css("border", "1px solid #F90A0A");
  }
}
function countryError(error) {
  if (!error) {
    $("#country").removeClass("valid taken");
    $("#country_err").hide();
    $("#country").css("border", "1px solid #34F458");
  } else {
    $("#country_err").text(error);
    $("#country_err").show();
    $("country").css("border", "1px solid #F90A0A");
  }
}
$("#country").blur(function () {
  var country = $(this).val();
  if (country === "") {
    countryError("Country name cannot be blank");
    return;
  } else if (!stateCountryPattern.test(country)) {
    countryError("Invalid country name");
    return;
  } else {
    countryError(null);
  }
});

$("#state").blur(function () {
  var state = $(this).val();
  if (state === "") {
    stateError("State name cannot be blank");
    return;
  } else if (!stateCountryPattern.test(state)) {
    stateError("Invalid State name");
    return;
  } else {
    stateError(null);
  }
});

$("#zip").blur(function () {
  var zip = $(this).val();
  if (zip === "") {
    zipError("Zip code cannot be blank");
    return;
  } else if (!zipPattern.test(zip)) {
    zipError("Invalid zipcode");
    return;
  } else {
    zipError(null);
  }
});

//Matching password and confirm passwords
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

// PROFILE EDIT
$("#edit-profile-button").click(function () {
  $("#profile-display").hide();
  $("#profile-edit-seg").css("display", "block");
  // $("#first_name_input").val($("#fnameinput").val())
  // $("#last_name_input").val($("#lnameinput").val())
  // $("#user-name").val($("#unameinput").val())
  // $("#user-email").val($("#emailinput").val())
  $("#user-phone_1").val($("#phoneinput").val());
});

$("#cancel-profile-edit").click(() => {
  $("#profile-display").show();
  $("#profile-edit-seg").css("display", "none");
});
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
      swal({ icon: "success", text: "Operation Aborted!" });
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
      swal({ icon: "success", text: "Operation Aborted!" });
    }
  });
}

//Block User, Re activate
function blockUser(userId) {
  swal({
    title: "Are you sure?",
    text: "The user will not be able to login until the user is approved again..!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/block-user/0".replace("0", parseInt(userId));
    } else {
      swal({ icon: "success", text: "Operation Aborted!" });
    }
  });
}
function reactivateUser(userId) {
  swal({
    title: "Are you sure?",
    text: "The user will be activated and can use the system.!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willActivate) => {
    if (willActivate) {
      window.location.href = "/reactivate-user/0".replace(
        "0",
        parseInt(userId)
      );
    } else {
      swal({ icon: "success", text: "Operation Aborted!" });
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
      swal({ icon: "success", text: "Operation Aborted!" });
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
      swal({ icon: "success", text: "Operation Aborted!" });
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
      swal({ icon: "success", text: "Operation Aborted!" });
    }
  });
}

function dispatchOrder(orderId) {
  swal({
    title: "Are you sure?",
    text: "The Order will be marked as dispatched!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDispatch) => {
    if (willDispatch) {
      window.location.href = "/ship-order/0".replace("0", parseInt(orderId));
    } else {
      swal({ icon: "info", text: "Operation Aborted!" });
    }
  });
}

function deliverOrder(orderId) {
  swal({
    title: "Are you sure?",
    text: "The Order will be marked as delivered!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      window.location.href = "/deliver-order/0".replace("0", parseInt(orderId));
    } else {
      swal({ icon: "info", text: "Operation Aborted!" });
    }
  });
}



//Show Books by categories
$("#book-categories").change(() => {
  var catId = $("#book-categories").find(":selected").val();
  if (catId) {
    window.location.href = "/show-books-categories/0".replace(
      "0",
      parseInt(catId)
    );
  }
});

// Checkout Page address
$("#checkout-edit-address-button").click(() => {
  $("#checkout-edit-address-button").hide();
  $("#checkout-address").hide();
  $("#checkout-edit-address").show();
});
$("#checkout-edit-address-cancel").click(() => {
  $("#checkout-address").show();
  $("#checkout-edit-address").hide();
  $("#checkout-edit-address-button").show();
});

$("#checkout-add-new-address-button").click(() => {
  $("#checkout-add-new-address-button").hide();
  $("#no-checkout-address").hide();
  $("#checkout-add-new-address").show();
});
$("#checkout-add-new-address-cancel").click(() => {
  $("#checkout-add-new-address-button").show();
  $("#no-checkout-address").show();
  $("#checkout-add-new-address").hide();
});
// Data tables ===
let table = new DataTable("#books-table", {scrollX: true});
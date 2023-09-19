from django.contrib import admin
from django.urls import path
from LibraryApp.views import *

urlpatterns = [
    # HOME
    path("", homePage, name="homePage"),
    path("search-items", searchBooks, name="searchBooks"),
    path("show-book/<int:pk>", showBook, name="showBook"),
    # PROFILE
    path("my-profile", myProfile, name="myProfile"),
    path("add-user-address", addUserAddress, name="addUserAddress"),
    path("edit-user-address", editUserAddress, name="editUserAddress"),
    path("update-image", updateImage, name="updateImage"),
    path('remove-profile-image', removeProfileImage, name= 'removeProfileImage'),
    # Reset Password
    path('reset-password',resetPassword, name='resetPassword'),
    # Username Email validation
    path("validate-email", validateEmail, name="validateEmail"),
    path("validate-username", validateUsername, name="validateUsername"),
    # SIGNIN AND SIGNUP
    path("signup/", signUpPage, name="signUpPage"),
    path("registerUser/", registerUser, name="registerUser"),
    path("sign-in/", signInPage, name="signInPage"),
    path("user-login/", userLogin, name="userLogin"),
    path("user-logout", userLogout, name="userLogout"),
    # CART OPERATIONS
    path("cart/", userCart, name="userCart"),
    path("add-to-cart", addToCart, name="addToCart"),
    path("remove-cart-item/<int:pk>", removeCartItem, name="removeCartItem"),
    path(
        "change-product-quantity", changeProductQuantity, name="changeProductQuantity"
    ),
    # RENT BOOK
    path("rent-book/<int:pk>", rentBook, name="rentBook"),
    path("checkout-rental", checkoutRental, name="checkoutRental"),
    path("rental-request-placed", rentalPlaced, name="rentalPlaced"),
    path("my-rental-history", rentalHistory, name="rentalHistory"),
    path("report-lost-book/<int:pk>/<int:ri>",reportLostBook, name = 'reportLostBook'),
    path('user-return-book/<int:rentalId>',userReturnBook, name='userReturnBook'),
    path('check-user-dues',checkDues, name= 'checkDues'),
    # Pay due and return book
    path('pay-due-and-return',payAndReturn, name='payAndReturn'),
    # Checkout
    path("checkout/", checkoutPage, name="checkoutPage"),
    path("place-order/", placeOrder, name="placeOrder"),
    # My Orders
    path("my-orders/", myOrders, name="myOrders"),
    # ADMIN PANEL FUNCTIONS AND OPERATIONS
    path("admin/", admin.site.urls),
    path("admin-home/", adminHomePage, name="adminHomePage"),
    path("show-user/", showUsers, name="showUsers"),
    path("reject-request/<int:pk>", rejectRequest, name="rejectRequest"),
    path("approve-request/<int:pk>", approveRequest, name="approveRequest"),
    # Purchases , Rental History
    path('user-purchase-history/<int:pk>',showUserPurchases, name= 'showUserPurchases'),
    path('user-rental-history/<int:pk>',showUserRental, name= 'showUserRental'),
    # Returned Books
    path('returned-books', returnedBooks, name= 'returnedBooks'),
    path('confirm-return/<int:rentalId>/<int:bookId>',confirmReturn, name= 'confirmReturn'),
    # Books
    path("show-books/", showBooks, name="showBooks"),
    path("add-new-book/", addNewBook, name="addNewBook"),
    path("add-book/", addBookDetails, name="addBookDetails"),
    path("edit-book/<int:pk>", editBookDetailsPage, name="editBookDetailsPage"),
    path("edit-book-details/<int:pk>", editBookDetails, name="editBookDetails"),
    path("remove-book/<int:pk>", removeBook, name="removeBook"),
    # ISBN Validation
    path('validate-isbn',validateISBN, name='validateISBN'),
    # Categories
    path("show-categories/", showCategories, name="showCategories"),
    path("add-new-category/", addNewCategoryPage, name="addNewCategoryPage"),
    path("add-category/", addCategoryDetails, name="addCategoryDetails"),
    path(
        "edit-category/<int:pk>",
        editCategoryDetailsPage,
        name="editCategoryDetailsPage",
    ),
    path(
        "edit-category-details/<int:pk>",
        editCategoryDetails,
        name="editCategoryDetails",
    ),
    path("remove-category/<int:pk>", removeCategory, name="removeCategory"),
    # Publisher
    path("show-publishers/", showPublishers, name="showPublishers"),
    path("add-new-publisher/", addNewPublisherPage, name="addNewPublisherPage"),
    path("add-publisher/", addPublisherDetails, name="addPublisherDetails"),
    path(
        "edit-publisher/<int:pk>",
        editPublisherDetailsPage,
        name="editPublisherDetailsPage",
    ),
    path(
        "edit-publisher-details/<int:pk>",
        editPublisherDetails,
        name="editPublisherDetails",
    ),
    path("remove-publisher/<int:pk>", removePublisher, name="removePublisher"),
]

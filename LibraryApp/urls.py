from django.contrib import admin
from django.urls import path
from LibraryApp.views import *

urlpatterns = [
    # HOME
    path('',homePage, name='homePage'),
    path('search-items',searchBooks, name= 'searchBooks'),
    path('show-book/<int:pk>',showBook, name= 'showBook'),

    # Username Email validation
    path('validate-email', validateEmail, name = 'validateEmail'),
    path('validate-username', validateUsername, name = 'validateUsername'),

    # SIGNIN AND SIGNUP
    path('signup/',signUpPage, name='signUpPage'),
    path('registerUser/',registerUser, name='registerUser'),
    path('sign-in/',signInPage, name='signInPage'),
    path('user-login/',userLogin, name='userLogin'),
    path('user-logout/',userLogout, name='userLogout'),

    # CART OPERATIONS
    path('cart/',userCart, name= 'userCart'),
    path('add-to-cart',addToCart, name='addToCart'),
    path('remove-cart-item/<int:pk>',removeCartItem, name='removeCartItem'),
    path('change-product-quantity',changeProductQuantity, name='changeProductQuantity'),

    # RENT BOOK
    path('rent-book/<int:pk>',rentBook, name='rentBook'),
    path('checkout-rental',checkoutRental, name='checkoutRental'),
    path('checkout-rental-page',checkoutRentalPage, name='checkoutRentalPage'),

    # Checkout
    path('checkout/',checkoutPage, name='checkoutPage'),
    path('place-order/',placeOrder, name='placeOrder'),

    # My Orders
    path('my-orders/',myOrders, name='myOrders'),

    # ADMIN PANEL FUNCTIONS AND OPERATIONS
    path('admin/', admin.site.urls),
    path('admin-home/',adminHomePage, name = 'adminHomePage'),
    path('user-approval-requests/',approveUserRequests, name='approveUserRequests'),
    path('reject-request/<int:pk>',rejectRequest, name='rejectRequest'),
    path('approve-request/<int:pk>',approveRequest, name='approveRequest'),

    # Books
    path('show-books/',showBooks, name='showBooks'),
    path('add-new-book/',addNewBook, name='addNewBook'),
    path('add-book/',addBookDetails,name='addBookDetails'),
    path('edit-book/<int:pk>',editBookDetailsPage, name='editBookDetailsPage'),
    path('edit-book-details/<int:pk>',editBookDetails, name='editBookDetails'),
    path('remove-book/<int:pk>',removeBook, name='removeBook'),

    # Categories
    path('show-categories/',showCategories, name='showCategories'),
    path('add-new-category/',addNewCategoryPage, name='addNewCategoryPage'),
    path('add-category/',addCategoryDetails,name='addCategoryDetails'),
    path('edit-category/<int:pk>',editCategoryDetailsPage, name='editCategoryDetailsPage'),
    path('edit-category-details/<int:pk>',editCategoryDetails, name='editCategoryDetails'),
    path('remove-category/<int:pk>',removeCategory, name='removeCategory'),

     # Publisher
    path('show-publishers/',showPublishers, name='showPublishers'),
    path('add-new-publisher/',addNewPublisherPage, name='addNewPublisherPage'),
    path('add-publisher/',addPublisherDetails,name='addPublisherDetails'),
    path('edit-publisher/<int:pk>',editPublisherDetailsPage, name='editPublisherDetailsPage'),
    path('edit-publisher-details/<int:pk>',editPublisherDetails, name='editPublisherDetails'),
    path('remove-publisher/<int:pk>',removePublisher, name='removePublisher'),
]
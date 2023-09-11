from django.contrib import admin
from django.urls import path
from LibraryApp.views import *

urlpatterns = [
    # HOME
    path('',homePage, name='homePage'),

    # Username Email validation
    path('validate-email', validateEmail, name = 'validateEmail'),
    path('validate-username', validateUsername, name = 'validateUsername'),

    # SIGNIN AND SIGNUP
    path('signup/',signUpPage, name='signUpPage'),
    path('registerUser/',registerUser, name='registerUser'),
    path('sign-in/',signInPage, name='signInPage'),
    path('user-login/',userLogin, name='userLogin'),
    path('user-logout/',userLogout, name='userLogout'),

    # ADMIN PANEL FUNCTIONS AND OPERATIONS
    path('admin/', admin.site.urls),
    path('admin-home/',adminHomePage, name = 'adminHomePage'),
    path('user-approval-requests/',approveUserRequests, name='approveUserRequests'),
    path('reject-request/<int:pk>',rejectRequest, name='rejectRequest'),
    path('approve-request/<int:pk>',approveRequest, name='approveRequest'),
]
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from random import randint
from .forms import SignUpForm, loginForm, UserCreationForm
from .models import *
from django.http import HttpResponse, JsonResponse

# from LibraryApp.forms import UserForm

# Create your views here.


# HOME
def homePage(request):
    return render(request, "user/home.html")


# Username Email validation
def validateEmail(request):
    if request.method == "POST":
        emailInput = request.POST.get("email")
        if User.objects.filter(email=emailInput).exists():
            return JsonResponse({"is_taken": True})
        else:
            return JsonResponse({"is_taken": False})


def validateUsername(request):
    if request.method == "POST":
        userNameInput = request.POST.get("username")
        if User.objects.filter(username=userNameInput).exists():
            return JsonResponse({"is_taken": True})
        else:
            return JsonResponse({"is_taken": False})


# SIGNIN AND SIGNUP
def signInPage(request):
    form = loginForm()
    context = {"form": form}
    return render(request, "user/login.html", context)


def signUpPage(request):
    form = SignUpForm()
    context = {"form": form}
    return render(request, "user/signup.html", context)

def registerUser(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone_number')
            password = str(randint(100000, 999999))
            user = form.save()
            reader = User.objects.get(id=user.id)
            readerData = Reader(user=reader, phone_number = phone, pass_reset_code=password)
            readerData.save()
            messages.success(request, 'Registration Successful. Login credentials will be sent via email once your account is approved.')

            return redirect("signInPage")
        else:
            messages.warning(request, 'Something went wrong..Please try again.')
            return redirect("signUpPage")
    else:
        messages.warning(request, 'Something went wrong..Please try again.')
        return redirect("signUpPage")


# def registerUser(request):
#     if request.method == "POST":
#         # form = SignUpForm(request.POST)
#         # if form.is_valid():
#         fName = request.POST["first_name"]
#         lName = request.POST["last_name"]
#         uName = request.POST["username"]
#         email = request.POST["email"]
#         password = str(randint(100000, 999999))
#         user = User.objects.create_user(
#             first_name=fName,
#             last_name=lName,
#             username=uName,
#             email=email,
#             password=password,
#         )

#         user.save()
#         reader = User.objects.get(id=user.id)
#         readerData = Reader(user=reader, pass_reset_code=password)
#         readerData.save()
#         # user = User.objects.create_user(first_name = fName, last_name = lName, username= uName, email= email)
#         # user.save()

#         return redirect("signInPage")
#     else:
#         return redirect("signUpPage")


def userLogin(request):
    try:
        next = request.GET.get("next")
    except:
        pass
    if request.method == "POST":
        username = request.POST.get("user-name")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect("adminHomePage")
                # return render(request, "admin-home.html", {"user": request.user})
            else:
                auth.login(request, user)
                if next:
                    return redirect(next)
                return redirect("homePage")
        else:
            messages.warning(request, "Incorrect Username or Password..Please try again")
            return redirect("signInPage")
    else:
        messages.warning(request, "Something went wrong..Please try again.")
        return redirect("signInPage")


@login_required(login_url="signInPage")
def userLogout(request):
    auth.logout(request)
    return redirect("signInPage")


# ADMIN PANEL OPERATIONS
def adminHomePage(request):
    return render(request, 'admin/home/admin-home.html')

@login_required(login_url='signInPage')
def approveUserRequests(request):
    users = Reader.objects.filter(is_approved = False)
    context= {
        "users":users
    }
    return render(request, 'admin/home/approval-request.html',context)

def rejectRequest(request,pk):
    reader = Reader.objects.get(user = pk)
    user = User.objects.get(id = pk)
    reader.delete()
    user.delete()

    messages.success(request, f'Sign In request of User ID - {pk} rejected successfully')
    return redirect('approveUserRequests')

def approveRequest(request,pk):
    reader = Reader.objects.get(user = pk)
    user = User.objects.get(id = pk)
    reader.is_approved = True
    user.set_password(str(reader.pass_reset_code))
    reader.save()
    user.save()
    
    # SEND MAIL CODE HERE
    subject = "REGISTRATION - Library Management System"
    message = f"Dear {user.first_name} {user.last_name},\nHope you are doing well.!\nYour Registration on the Library Management System is approved and you can login to the system with the credentials given below:\n\nUsername :{user.username}\nPassword:{reader.pass_reset_code}\n\nHappy Reading!!\n\n--\nRegards,\nADMIN\nLibrary Management System"
    recipient = user.email
    # send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

    messages.success(request, f'Sign In request of User ID - {pk} approved successfully')
    return redirect('approveUserRequests')

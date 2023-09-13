from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from random import randint
from .forms import SignUpForm, loginForm, UserCreationForm
from .forms import *
from .models import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse

# from LibraryApp.forms import UserForm

# Create your views here.


# HOME
def homePage(request):
    cartItemsCount = len(Cart.objects.filter(user=request.user.id))
    trending = Books.objects.all()[0:4]
    context = {"trending": trending, "count": cartItemsCount}
    return render(request, "user/home.html", context)


def searchBooks(request):
    if request.method == 'GET':
        key = request.GET['search']
        try:
            search_result = Books.objects.filter(Q(author__icontains = key)|Q(title__icontains = key))
        except:
            search_result = None
        return render(request,'user/search-books.html',{'search':search_result})
    else:
        return redirect('homePage')


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
            phone = form.cleaned_data.get("phone_number")
            password = str(randint(100000, 999999))
            user = form.save()
            reader = User.objects.get(id=user.id)
            readerData = Reader(
                user=reader, phone_number=phone, pass_reset_code=password
            )
            readerData.save()
            messages.success(
                request,
                "Registration Successful. Login credentials will be sent via email once your account is approved.",
            )

            return redirect("signInPage")
        else:
            messages.warning(request, "Something went wrong..Please try again.")
            return redirect("signUpPage")
    else:
        messages.warning(request, "Something went wrong..Please try again.")
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
            messages.error(request, "Incorrect Username or Password..Please try again")
            return redirect("signInPage")
    else:
        messages.error(request, "Something went wrong..Please try again.")
        return redirect("signInPage")


@login_required(login_url="signInPage")
def userLogout(request):
    auth.logout(request)
    return redirect("signInPage")


# CART OPERATIONS
@login_required(login_url="signInPage")
def userCart(request):
    cartItemsCount = len(Cart.objects.filter(user=request.user))
    books = Cart.objects.filter(user=request.user)
    netAmount = 0
    for i in books:
        netAmount += i.net_amount
    context = {"products": books, "count": cartItemsCount, "sum": netAmount}
    return render(request, "user/cart.html", context)


@login_required(login_url="signInPage")
def addToCart(request):
    if request.method == "POST":
        bookId = request.POST.get("book")
        book = Books.objects.get(id=bookId)
        user = User.objects.get(id=request.user.id)
        if Cart.objects.filter(user=user.id).exists():
            if Cart.objects.filter(user=user.id).filter(book=bookId).exists():
                # if product is not None:
                book = Cart.objects.get(user=user.id, book=bookId)
                book.quantity += 1
                book.net_amount = book.quantity * book.book.selling_price
                book.save()

                cartItemsCount = len(Cart.objects.filter(user=request.user.id))
                return JsonResponse(
                    {"status": "Item Added", "cartCount": cartItemsCount}
                )
            else:
                cartItem = Cart(
                    user=user, book=book, quantity=1, net_amount=book.selling_price
                )
                cartItem.save()

                cartItemsCount = len(Cart.objects.filter(user=request.user.id))
                return JsonResponse(
                    {"status": "Item Added", "cartCount": cartItemsCount}
                )
        else:
            cartItem = Cart(
                user=user, book=book, quantity=1, net_amount=book.selling_price
            )
            cartItem.save()

            cartItemsCount = len(Cart.objects.filter(user=request.user.id))
            return JsonResponse({"status": "Item Added", "cartCount": cartItemsCount})
    else:
        return redirect("homePage")


@login_required(login_url="signInPage")
def removeCartItem(request, pk):
    cartItem = Cart.objects.filter(user=request.user).filter(book=pk)
    cartItem.delete()
    messages.success(request, "Item Removed")
    return redirect("userCart")


def changeProductQuantity(request):
    if request.method == "POST":
        bookId = request.POST.get("book")
        count = request.POST.get("count")

        if Cart.objects.filter(user=request.user.id, book=bookId):
            cart = Cart.objects.get(user=request.user.id, book=bookId)
            cart.quantity += int(count)
            cart.net_amount = cart.quantity * cart.book.selling_price
            cart.save()
            items = Cart.objects.filter(user=request.user.id)
            netAmount = 0
            for i in items:
                netAmount += i.net_amount

            return JsonResponse(
                {"qty": cart.quantity, "totPrice": cart.net_amount, "sum": netAmount}
            )
    return redirect("userCart")


# CHECKOUT
@login_required(login_url="signInPage")
def checkoutPage(request):
    customer = Reader.objects.get(user=request.user)
    address = Address.objects.get(user=request.user)
    books = Cart.objects.filter(user=request.user.id)
    netAmount = 0
    for i in books:
        netAmount += i.net_amount
    count = len(books)

    context = {
        "count": count,
        "subtotal": netAmount,
        "customer": customer,
        "address": address,
    }
    return render(request, "user/checkout.html", context)


@login_required(login_url="signInPage")
def placeOrder(request):
    if request.method == "POST":
        items = Cart.objects.filter(user=request.user.id)
        for item in items:
            product = Books.objects.get(id=item.book.id)
            quantity = item.quantity
            price = item.net_amount
            order = Purchases(
                user=User.objects.get(id=request.user.id),
                book=product,
                amount=price,
                quantity=quantity,
                payment=request.POST["PaymentMethod"],
                purchase_status="Placed",
            )
            order.save()

        cart = Cart.objects.filter(user=request.user)
        cart.delete()
        items = Books.objects.all()[0:4]
        return render(request, "user/order-placed.html", {"items": items})
    else:
        messages.error(request, "Something went wrong, please try again.")
        return redirect("checkoutPage")


# ADMIN PANEL OPERATIONS
@login_required(login_url="signInPage")
def adminHomePage(request):
    return render(request, "admin/home/admin-home.html")


@login_required(login_url="signInPage")
def approveUserRequests(request):
    users = Reader.objects.filter(is_approved=False)
    context = {"users": users}
    return render(request, "admin/home/approval-request.html", context)


@login_required(login_url="signInPage")
def rejectRequest(request, pk):
    reader = Reader.objects.get(user=pk)
    user = User.objects.get(id=pk)
    reader.delete()
    user.delete()

    messages.success(
        request, f"Sign In request of User ID - {pk} rejected successfully"
    )
    return redirect("approveUserRequests")


@login_required(login_url="signInPage")
def approveRequest(request, pk):
    reader = Reader.objects.get(user=pk)
    user = User.objects.get(id=pk)
    reader.is_approved = True
    user.set_password(str(reader.pass_reset_code))
    reader.save()
    user.save()

    # SEND MAIL CODE HERE
    subject = "REGISTRATION - GreySense Library"
    message = f"Dear {user.first_name} {user.last_name},\nHope you are doing well.!\nYour Registration on the Library Management System is approved and you can login to the system with the credentials given below:\n\nUsername :{user.username}\nPassword:{reader.pass_reset_code}\n\nHappy Reading!!\n\n--\nRegards,\nADMIN\nGreySense Library"
    recipient = user.email
    # send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

    messages.success(
        request, f"Sign In request of User ID - {pk} approved successfully"
    )
    return redirect("approveUserRequests")


# BOOKS


@login_required(login_url="signInPage")
def showBooks(request):
    books = Books.objects.all()
    context = {"books": books}
    return render(request, "admin/book/show-books.html", context)


@login_required(login_url="signInPage")
def addNewBook(request):
    catg = Category.objects.all()
    publsh = Publisher.objects.all()
    context = {"categories": catg, "publishers": publsh}
    return render(request, "admin/book/add-book.html", context)


@login_required(login_url="signInPage")
def addBookDetails(request):
    if request.method == "POST":
        book = Books(
            book_number=request.POST["book-number"],
            title=request.POST["title"],
            edition=request.POST["edition"],
            author=request.POST["author"],
            summary=request.POST["summary"],
            category=Category.objects.get(id=request.POST["category"]),
            publisher=Publisher.objects.get(id=request.POST["publisher"]),
            year_of_publication=request.POST["yop"],
            list_price=request.POST["original-price"],
            selling_price=request.POST["selling-price"],
            rental_price=request.POST["rental-price"],
            stock_quantity=request.POST["quantity"],
            image=request.FILES.get("image"),
        )
        book.save()
        messages.success(request, "Book details added successfully.")
        return redirect("showBooks")
    else:
        messages.error(request, "Something went wrong. Please try again")
        return redirect("showBooks")


@login_required(login_url="signInPage")
def editBookDetailsPage(request, pk):
    book = Books.objects.get(id=pk)
    catg = Category.objects.all()
    publsh = Publisher.objects.all()
    context = {"book": book, "categories": catg, "publishers": publsh}
    return render(request, "admin/book/edit-book.html", context)


@login_required(login_url="signInPage")
def editBookDetails(request, pk):
    book = Books.objects.get(id=pk)

    if request.method == "POST":
        book.book_number = request.POST["book-number"]
        book.title = request.POST["title"]
        book.edition = request.POST["edition"]
        book.author = request.POST["author"]
        book.summary = request.POST["summary"]
        book.category = Category.objects.get(id=request.POST["category"])
        book.publisher = Publisher.objects.get(id=request.POST["publisher"])
        book.year_of_publication = request.POST["yop"]
        book.list_price = request.POST["original-price"]
        book.selling_price = request.POST["selling-price"]
        book.rental_price = request.POST["rental-price"]
        book.stock_quantity = request.POST["quantity"]
        newImage = request.FILES.get("image")
        currentImage = book.image
        if newImage is not None:
            book.image = newImage
        else:
            book.image = currentImage
        book.save()
        messages.success(request, "Book Data Updated Successfully.")
        return redirect("showBooks")
    else:
        messages.error(request, "Something went wrong, Please try again..")
        return redirect("showBooks")


@login_required(login_url="signInPage")
def removeBook(request, pk):
    book = Books.objects.get(id=pk)
    book.delete()
    messages.success(request, "Book Removed Successfully..")
    return redirect("showBooks")


# CATEGORIES


@login_required(login_url="signInPage")
def showCategories(request):
    ctg = Category.objects.all()
    context = {"categories": ctg}
    return render(request, "admin/category/show-categories.html", context)


@login_required(login_url="signInPage")
def addNewCategoryPage(request):
    return render(request, "admin/category/add-category.html")


@login_required(login_url="signInPage")
def addCategoryDetails(request):
    if request.method == "POST":
        category = Category(
            name=request.POST["category-name"],
            description=request.POST["category-description"],
        )
        category.save()

        messages.success(request, f"{category.name} category added successfully.")
        return redirect("showCategories")
    else:
        messages.error(request, "Something went wrong, Please try again.")
        return redirect("showCategories")


@login_required(login_url="signInPage")
def editCategoryDetailsPage(request, pk):
    category = Category.objects.get(id=pk)
    return render(request, "admin/category/edit-category.html", {"category": category})


@login_required(login_url="signInPage")
def editCategoryDetails(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        category.name = request.POST["category-name"]
        category.description = request.POST["category-description"]
        category.save()

        messages.success(
            request, f"{category.name} category details updated successfully."
        )
        return redirect("showCategories")
    else:
        messages.error(request, "Something went wrong, Please try again.")
        return redirect("showCategories")


@login_required(login_url="signInPage")
def removeCategory(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    messages.success(request, f"{category.name} Category removed successfully.")
    return redirect("showCategories")


# PUBLISHERS


@login_required(login_url="signInPage")
def showPublishers(request):
    publ = Publisher.objects.all()
    context = {"publishers": publ}
    return render(request, "admin/publisher/show-publishers.html", context)


@login_required(login_url="signInPage")
def addNewPublisherPage(request):
    return render(request, "admin/publisher/add-publisher.html")


@login_required(login_url="signInPage")
def addPublisherDetails(request):
    if request.method == "POST":
        publisher = Publisher(
            publisher_id=request.POST["id"],
            name=request.POST["name"],
        )
        publisher.save()

        messages.success(request, f"{publisher.name} Publisher added successfully.")
        return redirect("showPublishers")
    else:
        messages.error(request, "Something went wrong, Please try again.")
        return redirect("showPublishers")


@login_required(login_url="signInPage")
def editPublisherDetailsPage(request, pk):
    publisher = Publisher.objects.get(id=pk)
    return render(
        request, "admin/publisher/edit-publisher.html", {"publisher": publisher}
    )


@login_required(login_url="signInPage")
def editPublisherDetails(request, pk):
    publisher = Publisher.objects.get(id=pk)
    if request.method == "POST":
        publisher.publisher_id = request.POST["id"]
        publisher.name = request.POST["name"]
        publisher.save()

        messages.success(
            request, f"{publisher.name} Publisher details updated successfully."
        )
        return redirect("showPublishers")
    else:
        messages.error(request, "Something went wrong, Please try again.")
        return redirect("showPublishers")


@login_required(login_url="signInPage")
def removePublisher(request, pk):
    publisher = Publisher.objects.get(id=pk)
    publisher.delete()
    messages.success(request, f"{publisher.name} Category removed successfully.")
    return redirect("showPublishers")

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.contrib import messages
from random import randint
from .forms import SignUpForm, loginForm, UserCreationForm
from .forms import *
from .models import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from datetime import date, datetime, timedelta

# from LibraryApp.forms import UserForm

# Create your views here.


# HOME
def homePage(request):
    cartItemsCount = len(Cart.objects.filter(user=request.user.id))
    try:
        reader = Reader.objects.get(user=request.user.id)
    except:
        reader = None
    trending = Books.objects.all()[0:4]
    try:
        dues = overDues(request.user.id)
    except:
        dues = None
    try:
        nearingDues = alertDues(request.user.id)
    except:
        nearingDues = None
    books = Books.objects.all()
    context = {
        "trending": trending,
        "count": cartItemsCount,
        "reader": reader,
        "dues": dues,
        "books":books,
        "nearingDues": nearingDues,
        "duesCount": len(dues) + len(nearingDues),
    }
    return render(request, "user/home.html", context)


def searchBooks(request):
    if request.method == "GET":
        key = request.GET["search"]
        try:
            search_result = Books.objects.filter(
                Q(author__icontains=key) | Q(title__icontains=key)
            )
        except:
            search_result = None
        return render(request, "user/search-books.html", {"search": search_result})
    else:
        return redirect("homePage")


# Book details
def showBook(request, pk):
    prd = Books.objects.get(id=pk)
    cartItemsCount = len(Cart.objects.filter(user=request.user.id))
    # ctg = Category.objects.all()
    items = Books.objects.filter(category=prd.category.id)[0:4]
    context = {
        # "categories": ctg,
        "count": cartItemsCount,
        "book": prd,
        "items": items,
    }
    return render(request, "user/book.html", context)


# PROFILE
def myProfile(request):
    try:
        address = Address.objects.get(user=request.user.id)
    except:
        address = None
    reader = Reader.objects.get(user=request.user.id)
    context = {
        "user": User.objects.get(id=request.user.id),
        "address": address,
        "reader": reader,
    }
    return render(request, "user/profile.html", context)


# Address


def addUserAddress(request):
    if request.method == "POST":
        address = Address(
            user=User.objects.get(id=request.user.id),
            apartment_flat_suite=request.POST["house-flat"],
            street_address=request.POST["street"],
            city=request.POST["city"],
            state=request.POST["state"],
            country=request.POST["country"],
            zipcode=request.POST["zip"],
        )
        address.save()

        messages.success(request, "Address added successfully.")
        return redirect("myProfile")
    else:
        messages.error(request, "Something went wrong, Please try again.!")
        return redirect("myProfile")


def editUserAddress(request):
    if request.method == "POST":
        address = Address.objects.get(user=request.user.id)
        address.apartment_flat_suite = request.POST["house-flat"]
        address.street_address = request.POST["street"]
        address.city = request.POST["city"]
        address.state = request.POST["state"]
        address.country = request.POST["country"]
        address.zipcode = request.POST["zip"]
        address.save()

        messages.success(request, "Address updated successfully.")
        return redirect("myProfile")
    else:
        messages.error(request, "Something went wrong, Please try again.!")
        return redirect("myProfile")


def updateImage(request):
    if request.method == "POST":
        newImage = request.FILES.get("image")
        reader = Reader.objects.get(user=request.user.id)
        reader.image = newImage
        reader.save()
        messages.success(request, "Image updated Successfully.")
        return redirect("myProfile")
    else:
        messages.error(request, "Something went wrong, Please try again.!")
        return redirect("myProfile")


def removeProfileImage(request):
    reader = Reader.objects.get(user=request.user.id)
    reader.image = None
    reader.save()
    messages.success(request, "Photo Removed.!")
    return redirect("myProfile")


# RESET PASSWORD
@login_required(login_url="signInPage")
def resetPassword(request):
    if request.method == "POST":
        current = request.POST.get("currentPassword")
        new = request.POST.get("newPassword")
        confirm = request.POST.get("confirmPassword")
        reader = Reader.objects.get(user=request.user.id)
        if reader.pass_reset_code != current:
            return JsonResponse(
                {"status": False, "message": "Current password given is incorrect.!"}
            )
        else:
            if new != confirm:
                return JsonResponse(
                    {"status": False, "message": "Both password fields should match!"}
                )
            else:
                reader.pass_reset_code = new
                reader.save()
                user = User.objects.get(id=request.user.id)
                user.set_password(new)
                user.save()
                return JsonResponse(
                    {"status": True, "message": "Password Updated Successfully."}
                )
    else:
        return JsonResponse(
            {"status": False, "message": "Something went wrong, Please try again.!"}
        )


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


def is_admin(user):
    if user.groups.filter(name="ADMIN").exists():
        return True
    else:
        # return HttpResponse(messages.warning('message','You are not allowed to access this page.!'))
        return False


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
                stock = Books.objects.get(id=bookId)
                stock.stock_quantity -= 1
                stock.save()

                cartItemsCount = len(Cart.objects.filter(user=request.user.id))
                return JsonResponse(
                    {
                        "status": "Item Added",
                        "cartCount": cartItemsCount,
                        "stock": stock.stock_quantity,
                    }
                )
            else:
                cartItem = Cart(
                    user=user, book=book, quantity=1, net_amount=book.selling_price
                )
                cartItem.save()
                stock = Books.objects.get(id=bookId)
                stock.stock_quantity -= 1
                stock.save()

                cartItemsCount = len(Cart.objects.filter(user=request.user.id))
                return JsonResponse(
                    {
                        "status": "Item Added",
                        "cartCount": cartItemsCount,
                        "stock": stock.stock_quantity,
                    }
                )
        else:
            cartItem = Cart(
                user=user, book=book, quantity=1, net_amount=book.selling_price
            )
            cartItem.save()
            stock = Books.objects.get(id=bookId)
            stock.stock_quantity -= 1
            stock.save()

            cartItemsCount = len(Cart.objects.filter(user=request.user.id))
            return JsonResponse(
                {
                    "status": "Item Added",
                    "cartCount": cartItemsCount,
                    "stock": stock.stock_quantity,
                }
            )
    else:
        return redirect("homePage")


@login_required(login_url="signInPage")
def removeCartItem(request, pk):
    cartItem = Cart.objects.get(user=request.user, book=pk)
    stock = Books.objects.get(id=pk)
    stock.stock_quantity += cartItem.quantity
    stock.save()
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
            book = Books.objects.get(id=bookId)
            book.stock_quantity -= int(count)
            book.save()
            items = Cart.objects.filter(user=request.user.id)
            netAmount = 0
            for i in items:
                netAmount += i.net_amount

            return JsonResponse(
                {
                    "qty": cart.quantity,
                    "totPrice": cart.net_amount,
                    "sum": netAmount,
                    "stock": book.stock_quantity,
                }
            )
    return redirect("userCart")


# RENT BOOK
@login_required(login_url='signInPage')
def rentBook(request, pk):
    book = Books.objects.get(id=pk)
    context = {"book": book}
    return render(request, "user/rental.html", context)

@login_required(login_url='signInPage')
def checkoutRental(request):
    if request.method == "POST":
        bookId = request.POST.get("book")
        dueDate = request.POST.get("dueDate")
        amount = request.POST.get("amount")
        days = request.POST.get("days")
        paymentMethod = request.POST.get("payment")
        dDate = date.today() + timedelta(int(days))

        rental = Rental(
            user=User.objects.get(id=request.user.id),
            book=Books.objects.get(id=bookId),
            due_date=dDate,
            rental_amount=amount,
            payment=paymentMethod,
            status="Active",
        )
        rental.save()
        stock = Books.objects.get(id=bookId)
        stock.stock_quantity -= 1
        stock.save()
        # Send Mail code here...

        return JsonResponse({"status": True})
    else:
        return JsonResponse({"status": False})

@login_required(login_url='signInPage')
def rentalPlaced(request):
    book = Rental.objects.filter(user=request.user.id).last()
    return render(request, "user/rental-confirm.html", {"id": book.id})

@login_required(login_url='signInPage')
def rentalHistory(request):
    rental = Rental.objects.filter(user=request.user.id).order_by("-id")
    context = {"rental": rental}
    return render(request, "user/rental-history.html", context)


# LOST BOOK
@login_required(login_url='signInPage')
def reportLostBook(request, pk, ri):
    book = Books.objects.get(id=pk)
    amount = float(book.selling_price) + float(book.selling_price) * 0.03
    penalty = Penalty(
        user=User.objects.get(id=request.user.id),
        book=Books.objects.get(id=pk),
        amount=amount,
    )
    penalty.save()
    rental = Rental.objects.get(id=ri)
    rental.is_lost = True
    rental.status = "Book Lost"
    rental.fine_amount = amount
    rental.save()
    messages.info(
        request, "The Book is marked as lost and the penalty has been assigned to you."
    )
    return redirect("rentalHistory")

@login_required(login_url='signInPage')
def userReturnBook(request, rentalId):
    returnItem = Rental.objects.get(id=rentalId)
    returnItem.is_user_returned = True
    returnItem.return_date = date.today()
    returnItem.status = "Pending return confirmation"
    returnItem.save()
    messages.info(
        request, "The Book will be marked as returned after the confirmation from ADMIN"
    )
    return redirect("rentalHistory")

@login_required(login_url='signInPage')
def payAndReturn(request):
    if request.method == "POST":
        rentalItem = Rental.objects.get(id=request.POST["rental-id-due-payment"])
        rentalItem.return_date = date.today()
        rentalItem.is_due_cleared = True
        rentalItem.status = "Pending return confirmation"
        rentalItem.is_user_returned = True
        rentalItem.save()
        messages.success(
            request,
            "Payment has been completed, Return process will be completed after ADMIN confirmed.",
        )
        return redirect("rentalHistory")
    else:
        messages.error(request, "Something went wrong, Please try again.!")
        return redirect("rentalHistory")


def get_date_difference(today, dueDate):
    diff = dueDate - today
    return diff.days


# Items due in 0-3 days
def alertDues(user):
    idList = []
    items = Rental.objects.filter(user=user).filter(
        Q(is_lost=False)
        & Q(is_returned=False)
        & Q(is_overdue=False)
        & Q(is_user_returned=False)
    )
    for i in items:
        if (
            get_date_difference(date.today(), i.due_date) >= 0
            and get_date_difference(date.today(), i.due_date) <= 3
        ):
            idList.append(i.id)

    alertItems = Rental.objects.filter(id__in=idList)
    return alertItems


def overDues(user):
    idList = []
    items = Rental.objects.filter(user=user).filter(
        Q(is_lost=False)
        & Q(is_returned=False)
        & Q(is_overdue=True)
        & Q(is_user_returned=False)
    )
    for i in items:
        if get_date_difference(date.today(), i.due_date) < 0:
            idList.append(i.id)

    alertItems = Rental.objects.filter(id__in=idList)
    return alertItems


def checkDues(user):
    rentalItems = Rental.objects.filter(user=user).filter(
        Q(is_lost=False)
        & Q(is_returned=False)
        & Q(is_user_returned=False)
        & Q(is_due_cleared=False)
    )
    for item in rentalItems:
        dueDate = item.due_date
        diff = get_date_difference(date.today(), dueDate)
        if diff < 0:
            item.is_overdue = True
            item.status = "Overdue"
            if diff < 0 and diff >= -5:
                fine = abs(diff) * 5
                item.fine_amount = fine
            elif diff <= -6 and diff >= -10:
                fine = abs(diff) * 6
                item.fine_amount = fine
            else:
                fine = 100
                item.fine_amount = 100
        item.save()
    return rentalItems


# Fetching overdue renal details for ADMIN
def getOverDues():
    rentalItems = Rental.objects.filter(
        Q(is_lost=False)
        & Q(is_returned=False)
        & Q(is_user_returned=False)
        & Q(is_due_cleared=False)
    )
    id_list = []
    for item in rentalItems:
        dueDate = item.due_date
        diff = get_date_difference(date.today(), dueDate)
        if diff < 0:
            id_list.append(item.id)
            item.is_overdue = True
            item.status = "Overdue"
            if diff < 0 and diff >= -5:
                fine = abs(diff) * 5
                item.fine_amount = fine
            elif diff <= -6 and diff >= -10:
                fine = abs(diff) * 6
                item.fine_amount = fine
            else:
                fine = 100
                item.fine_amount = 100
        item.save()
    dues = Rental.objects.filter(id__in=id_list)
    return dues


# CHECKOUT
@login_required(login_url="signInPage")
def checkoutPage(request):
    customer = Reader.objects.get(user=request.user)
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
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
            # product.stock_quantity -=quantity
            # product.save()

        # Order details mail here

        cart = Cart.objects.filter(user=request.user)
        cart.delete()
        items = Books.objects.all()[0:4]
        return render(
            request, "user/order-placed.html", {"items": items, "id": order.id}
        )
    else:
        messages.error(request, "Something went wrong, please try again.")
        return redirect("checkoutPage")


# ORDERS
@login_required(login_url='signInPage')
def myOrders(request):
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    orders = Purchases.objects.filter(user=request.user).order_by("-id")
    context = {"orders": orders, "address": address}
    return render(request, "user/orders.html", context)


# ADMIN PANEL OPERATIONS
@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def adminHomePage(request):
    requests = Reader.objects.filter(is_approved=False)
    try:
        dues = getOverDues
    except:
        dues = None
    try:
        returned = Rental.objects.filter(
            Q(is_user_returned=True) & Q(is_returned=False)
        )
    except:
        returned = None
    print('dues===',dues)
    context = {"requests": requests, "returned": returned, "dues": dues}
    return render(request, "admin/home/admin-home.html", context)


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def showUsers(request):
    requests = Reader.objects.filter(is_approved=False)
    users = Reader.objects.all()
    context = {"requests": requests, "users": users}
    return render(request, "admin/user/users.html", context)


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def rejectRequest(request, pk):
    reader = Reader.objects.get(user=pk)
    user = User.objects.get(id=pk)
    reader.delete()
    user.delete()

    messages.success(
        request, f"Sign In request of User ID - {pk} rejected successfully"
    )
    return redirect("showUsers")


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
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
    return redirect("showUsers")


# HISTORY -- Purchase, rental


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def showUserPurchases(request, pk):
    purchaseItems = Purchases.objects.filter(user=pk)
    context = {"items": purchaseItems}
    return render(request, "admin/user/user-purchase.html", context)


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def showUserRental(request, pk):
    rentalItems = Rental.objects.filter(user=pk)
    context = {"items": rentalItems}
    return render(request, "admin/user/user-rental.html", context)


# Book returned
@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def returnedBooks(request):
    returnedBooks = Rental.objects.filter(
        Q(is_user_returned=True) & Q(is_returned=False)
    )
    context = {"returned": returnedBooks}
    return render(request, "admin/user/returned-book.html", context)


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def confirmReturn(request, rentalId, bookId):
    record = Rental.objects.get(id=rentalId)
    book = Books.objects.get(id=bookId)
    record.is_returned = True
    record.status = "Returned"
    book.stock_quantity += 1
    record.save()
    book.save()

    messages.success(request, "Book return confirmed.")
    return redirect("returnedBooks")


# BOOKS


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def showBooks(request):
    books = Books.objects.all()
    context = {"books": books}
    return render(request, "admin/book/show-books.html", context)


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def addNewBook(request):
    catg = Category.objects.all()
    publsh = Publisher.objects.all()
    context = {"categories": catg, "publishers": publsh}
    return render(request, "admin/book/add-book.html", context)


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def addBookDetails(request):
    if request.method == "POST":
        book = Books(
            isbn=request.POST["book-number"],
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
@user_passes_test(is_admin, login_url="signInPage")
def editBookDetailsPage(request, pk):
    book = Books.objects.get(id=pk)
    catg = Category.objects.all()
    publsh = Publisher.objects.all()
    context = {"book": book, "categories": catg, "publishers": publsh}
    return render(request, "admin/book/edit-book.html", context)


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def editBookDetails(request, pk):
    book = Books.objects.get(id=pk)

    if request.method == "POST":
        book.isbn = request.POST["book-number"]
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
@user_passes_test(is_admin, login_url="signInPage")
def removeBook(request, pk):
    book = Books.objects.get(id=pk)
    book.delete()
    messages.success(request, "Book Removed Successfully..")
    return redirect("showBooks")

# ISBN Validation
def validateISBN(request):
    if request.method == "POST":
        isbnInput = request.POST.get("isbn")
        if Books.objects.filter(isbn=isbnInput).exists():
            return JsonResponse({"is_taken": True})
        else:
            return JsonResponse({"is_taken": False})
    else:
        return redirect('addNewBook')

# CATEGORIES


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def showCategories(request):
    ctg = Category.objects.all()
    context = {"categories": ctg}
    return render(request, "admin/category/show-categories.html", context)


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def addNewCategoryPage(request):
    return render(request, "admin/category/add-category.html")


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
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
@user_passes_test(is_admin, login_url="signInPage")
def editCategoryDetailsPage(request, pk):
    category = Category.objects.get(id=pk)
    return render(request, "admin/category/edit-category.html", {"category": category})


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
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
@user_passes_test(is_admin, login_url="signInPage")
def removeCategory(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    messages.success(request, f"{category.name} Category removed successfully.")
    return redirect("showCategories")


# PUBLISHERS


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def showPublishers(request):
    publ = Publisher.objects.all()
    context = {"publishers": publ}
    return render(request, "admin/publisher/show-publishers.html", context)


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
def addNewPublisherPage(request):
    return render(request, "admin/publisher/add-publisher.html")


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
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
@user_passes_test(is_admin, login_url="signInPage")
def editPublisherDetailsPage(request, pk):
    publisher = Publisher.objects.get(id=pk)
    return render(
        request, "admin/publisher/edit-publisher.html", {"publisher": publisher}
    )


@login_required(login_url="signInPage")
@user_passes_test(is_admin, login_url="signInPage")
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
@user_passes_test(is_admin, login_url="signInPage")
def removePublisher(request, pk):
    publisher = Publisher.objects.get(id=pk)
    publisher.delete()
    messages.success(request, f"{publisher.name} Category removed successfully.")
    return redirect("showPublishers")

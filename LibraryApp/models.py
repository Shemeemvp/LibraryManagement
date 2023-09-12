from django.db import models
from django.contrib.auth.models import User, auth
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    apartment_flat_suite = models.CharField(max_length=100)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=100)
    zipcode = models.IntegerField()

# class SignUpModel(models.Model):
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     username = models.CharField(max_length=150)
#     email = models.EmailField(max_length=200)
#     phone_number = PhoneNumberField()

class Reader(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, on_delete=models.PROTECT, null=True, blank=True
    )
    phone_number = PhoneNumberField()
    pass_reset_code = models.BigIntegerField()
    image = models.ImageField(upload_to='users/',null=True)
    is_approved = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50,null=True,blank=True)


class Publisher(models.Model):
    publisher_id = models.BigIntegerField()
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100,null=True,blank=True)


class Books(models.Model):
    book_number = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100,null=True,blank=True)
    edition = models.IntegerField(null=True)
    author = models.CharField(max_length=150)
    summary = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT)
    year_of_publication = models.IntegerField()
    list_price = models.DecimalField(max_digits=6, decimal_places=2)
    selling_price = models.DecimalField(max_digits=6, decimal_places=2)
    rental_price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to="books/")
    is_recommended = models.BooleanField(default=False)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    net_amount = models.DecimalField(max_digits=6, decimal_places=2)


class Purchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey(Books, on_delete=models.PROTECT)
    purchase_date = models.DateField(auto_now_add=True, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment = models.CharField(max_length=20)
    purchase_status = models.CharField(max_length=20)


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey(Books, on_delete=models.PROTECT)
    reserve_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True)
    return_date = models.DateField(null=True)
    is_lost = models.BooleanField(default=False)
    is_overdue = models.BooleanField(default=False)


class Penalty(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey(Books, on_delete=models.PROTECT)
    rental_data = models.ForeignKey(Rental, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    penalized_date = models.DateField(null=True)
    is_paid = models.BooleanField(default=False)

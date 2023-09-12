from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class SignUpForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial='IN')
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({
            "required":True,
            'name':'first_name',
            'id':'first_name_input',
            "class":'form-control',
            'placeholder':'First Name',
            'type':'text'
        })
        self.fields["last_name"].widget.attrs.update({
            "required":False,
            'name':'last_name',
            'id':'last_name_input',
            "class":'form-control',
            'placeholder':'Last Name',
            'type':'text'
        })
        self.fields["username"].widget.attrs.update({
            "required":True,
            'name':'username',
            'id':'user-name',
            "class":'form-control',
            'placeholder':'User Name',
            'type':'text'
        })
        self.fields["email"].widget.attrs.update({
            "required":True,
            'name':'email',
            'id':'user-email',
            "class":'form-control',
            'placeholder':'Email Address',
            'type':'email'
        })
        self.fields["phone_number"].widget.attrs.update({
            "required":True,
            'name':'phone_number',
            'id':'user-phone',
            "class":'form-control',
            "type":"tel",
            'placeholder':'Contact Number',
        })
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=200, help_text=None)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username","email"]
        # fields = "__all__"

class loginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ["username"]


# class SignUpForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["password1"].help_text = None
#         self.fields["password2"].help_text = None

#     class Meta:
#         email = forms.EmailField(required=True)
#         model = User
#         fields = ["first_name", "last_name", "username", "email"]
#         help_texts = {
#             "username": None,
#             "email": None,
#             "password1": None,
#             "password2": None,
#         }

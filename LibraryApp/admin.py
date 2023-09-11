from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Publisher)
class PublisherModelAdmin(admin.ModelAdmin):
    list_display=('publisher_id','name')
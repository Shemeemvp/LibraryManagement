# Generated by Django 4.2.3 on 2023-09-15 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0010_rental_rental_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='payment',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='rental',
            name='status',
            field=models.CharField(max_length=30, null=True),
        ),
    ]

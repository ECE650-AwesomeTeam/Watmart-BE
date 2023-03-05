from django.db import models
<<<<<<< HEAD
=======
from django.conf import settings
import os
>>>>>>> dc11c7c6e52fc6476912a179dbb55bf55670ac0c

# Create your models here.

class User(models.Model):
    # Enum for Gender
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

    # Enum for Occupation
    STUDENT = 'STU'
    FACULTY = 'FAC'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (FACULTY, 'Faculty'),
    ]

    # Attributes
    email = models.EmailField(
        unique=True,
        primary_key=True
    )
    fname = models.CharField(
        max_length=16
    )
    lname = models.CharField(
        max_length=16
    )
    birthday = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    wat_id = models.CharField(
        max_length=8,
        blank=True,
        null=True
    )
    occupation = models.CharField(
        max_length=3,
        choices=OCCUPATION_CHOICES,
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

class Password(models.Model):
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        primary_key=True
    )
    # 128-bit = 32-hex
    md5_pwd = models.CharField(
        max_length=32
    )
    token = models.FileField(
        max_length=255,
        null=True
    )


class Product(models.Model):
    # Enum for status
    AVAILABLE = 'A'
    SOLD = 'S'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]

    # Enum for category
    ELECTRONICS = 'ELEC'
    FURNITURE = 'FURN'
    CLOTHING = 'CLOT'
    BOOKS = 'BOOK'
    SPORTS = 'SPOR'
    COLLECTIONS = 'COLL'
    INSTRUMENTS = 'INTR'
    ACCESSORIES = 'ACCE'
    APPLIANCES = 'APPL'
    CATEGORY_CHOICES = [
        (ELECTRONICS, 'Electronics'),
        (FURNITURE, 'Furniture'),
        (CLOTHING, 'Clothing'),
        (BOOKS, 'Books'),
        (SPORTS, 'Sports'),
        (COLLECTIONS, 'Collections'),
        (INSTRUMENTS, 'Music Instruments'),
        (ACCESSORIES, 'Accessories'),
        (ACCESSORIES, 'Home Appliances'),
    ]

    id = models.AutoField(
        primary_key=True
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(
        auto_now=True
    )
    price = models.FloatField()
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES
    )
    title = models.CharField(
        max_length=100
    )
    content = models.CharField(
        max_length=1000
    )
    category = models.CharField(
        max_length=4,
        choices=CATEGORY_CHOICES
    )


def get_url(instance, filename):
    return os.path.join(str(instance.product.id), filename)

class Image(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )
    file = models.ImageField(
        upload_to = get_url,
    )

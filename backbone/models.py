from django.db import models
from django.conf import settings
import os


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
    PENDING = 'P'
    SOLD = 'S'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (PENDING, 'Pending'),
        (SOLD, 'Sold'),
    ]

    # Enum for category
    ELECTRONICS = 'ELEC'
    FURNITURE = 'FURN'
    CLOTHING = 'CLOT'
    BOOKS = 'BOOK'
    SPORTS = 'SPOR'
    COLLECTIBLES = 'COLL'
    INSTRUMENTS = 'INTR'
    ACCESSORIES = 'ACCE'
    APPLIANCES = 'APPL'
    CATEGORY_CHOICES = [
        (ELECTRONICS, 'Electronics'),
        (FURNITURE, 'Furniture'),
        (CLOTHING, 'Clothing'),
        (BOOKS, 'Books'),
        (SPORTS, 'Sports'),
        (COLLECTIBLES, 'Collectibles'),
        (INSTRUMENTS, 'Instruments'),
        (ACCESSORIES, 'Accessories'),
        (ACCESSORIES, 'Appliances'),
    ]

    # Enum for quality
    NEW = 'N'
    USED = 'U'
    QUALITY_CHOICES= [
        (NEW, 'New'),
        (USED, 'Used')
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
    quality = models.CharField(
        max_length=1,
        choices=QUALITY_CHOICES
    )


class Order(models.Model):
    VALID = 'V'
    CANCELLED = 'C'
    STATUS_CHOICES = [
        (VALID, 'Valid'),
        (CANCELLED, 'Cancelled'),
    ]
    id = models.AutoField(
        primary_key=True
    )
    seller = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='seller',
        default=""
    )
    buyer = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='buyer',
        default="")
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(
        auto_now=True
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=""
    )
    note = models.CharField(
        max_length=1000,
        default="",
        null=True
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
        upload_to=get_url,
    )

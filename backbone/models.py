from django.db import models

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
    name = models.CharField(
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
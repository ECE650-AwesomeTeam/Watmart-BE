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

    # Enum for Major
    # TODO

    # Enum for Occupation
    STUDENT = 'STU'
    FACULTY = 'FAC'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (FACULTY, 'Faculty'),
    ]

    # Attributes
    name = models.CharField(
        max_length=16
    )
    email = models.EmailField()
    birthday = models.DateField(
        blank=True,
        null=True
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=OTHER
    )
    major = models.CharField(
        max_length=16,
        default=''
    )
    occupation = models.CharField(
        max_length=3,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    phone = models.CharField(
        max_length=10,
        default=''
    )

class Password(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        primary_key=True
    )
    # 128-bit = 32-hex
    md5_pwd = models.CharField(
        max_length=32
    )
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from backbone.models import User
from backbone.models import Password

# Create your views here.
@csrf_exempt
def signup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    birthday = request.POST.get('birthday')
    password = request.POST.get('password')
    gender = request.POST.get('gender')
    major = request.POST.get('major')
    occ = request.POST.get('occupation')
    phone = request.POST.get('phone')

    create_user(name, email, birthday, password, gender, major, occ, phone)
    return HttpResponse('User profile created successfully!')


def create_user(name, email, birthday, password, gender=None, major=None, occ=None, phone=None):
    user = User()
    user.name = name
    user.email = email
    user.birthday = birthday
    user.gender = gender
    user.major = major
    user.occupation = occ
    user.phone = phone
    user.save()

    pwd = Password()
    pwd.user = user
    pwd.md5_pwd = password
    pwd.save()


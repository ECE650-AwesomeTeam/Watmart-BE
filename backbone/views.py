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
    wat_id = request.POST.get('watcard_id')
    occ = request.POST.get('occupation')
    phone = request.POST.get('phone')

    if create_user(name, email, birthday, password, gender, wat_id, occ, phone):
        return HttpResponse('User profile created successfully!')
    else:
        return HttpResponse('Failed')


def create_user(name, email, birthday, password, gender, wat_id, occ, phone):
    if all([name, email, birthday, password]):
        user = User()
        user.name = name
        user.email = email
        user.birthday = birthday
        user.gender = gender
        user.wat_id = wat_id
        user.occupation = occ
        user.phone = phone
        user.save()

        pwd = Password()
        pwd.user = user
        pwd.md5_pwd = password
        pwd.save()

        return 1
    else:
        return 0


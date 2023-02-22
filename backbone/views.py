from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponseServerError
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from backbone.models import User
from backbone.models import Password
import json


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fname = data['firstName']
        lname = data['lastName']
        email = data['email']
        birthday = data['birthday']
        password = data['password']
        gender = data['gender']
        wat_id = data['watcardID']
        occ = data['occupation']
        phone = data['phone']

        respose = {
            'msg': None,
        }

        status = create_user(fname, lname, email, birthday, password,
                             gender, wat_id, occ, phone)
        if status == 1:
            respose['msg'] = 'User created successfully!'
            return HttpResponse(json.dumps(respose))
        elif status == -1:
            respose['msg'] = 'Current email has already been registered.'
            return HttpResponseServerError(json.dumps(respose))
        else:
            respose['msg'] = 'Failed'
            return HttpResponseServerError(json.dumps(respose))
    return HttpResponseNotAllowed(['POST'])


def create_user(fname, lname, email, birthday, password, gender, wat_id, occ, phone):
    """Create a user entity in the database.

    Returns:
        1: create successfully
        0: mandatory fields are empty
        -1: pk exists
    """
    if all([fname, lname, email, birthday, password]):
        if (User.objects.filter(email=email)):
            return -1
        user = User()
        user.fname = fname
        user.lname = lname
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


def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        verify = Password.objects.filter(user_id=email, md5_pwd=password)
        respose = {
            'msg': None,
        }
        if verify:
            respose['msg'] = 'Log in successfully!'
            return HttpResponse(json.dumps(respose))
        else:
            respose['msg'] = 'User does not exist or the password does not match'
            return HttpResponseServerError(json.dumps(respose))
    return HttpResponseNotAllowed(['POST'])


from django.shortcuts import render
from django.shortcuts import HttpResponse
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
            'status': None
        }

        status = create_user(fname, lname, email, birthday, password,
                             gender, wat_id, occ, phone)
        if status == 1:
            respose['msg'] = 'User created successfully!'
            respose['status'] = 200000
        elif status == -1:
            respose['msg'] = 'Current email has already been registered.'
            respose['status'] = 100001
        else:
            respose['msg'] = 'Failed'
            respose['status'] = 100002
        
        return HttpResponse(json.dumps(respose))


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


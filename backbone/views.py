from django.shortcuts import render
from django.shortcuts import HttpResponse
<<<<<<< HEAD
from django.http import HttpResponseServerError
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from backbone.models import User
from backbone.models import Password
import json
=======
from django.http import HttpResponseServerError, JsonResponse
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from backbone.models import User
from backbone.models import Password
from backbone.models import Product
from backbone.models import Image
import json
import shutil
import os
import jwt
>>>>>>> dc11c7c6e52fc6476912a179dbb55bf55670ac0c


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

<<<<<<< HEAD
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


=======
        status = create_user(fname, lname, email, birthday, password,
                             gender, wat_id, occ, phone)
        if status == 1:
            return HttpResponse('User created successfully!')
        elif status == -1:
            return HttpResponseServerError('Current email has already been registered.')
        else:
            return HttpResponseServerError('Failed')
    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        verify = Password.objects.filter(user_id=email, md5_pwd=password)
        if verify:
            a = Password.objects.get(user_id=email)
            b = {'email': email, 'password': password}
            token = jwt.encode(b, 'secret', algorithm='HS256')
            a.token = token
            a.save()
            return JsonResponse({'msg': 'Log in successfully', 'token': token})
        else:
            return HttpResponse('User does not exist or the password does not match')
    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        files = request.FILES.getlist('img')

        email = request.POST.get('user')
        price = request.POST.get('price')
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')

        user = User.objects.filter(email=email)
        if not user.exists():
            return HttpResponseServerError('User does not exist.')
        user = user[0]
        product = Product(
            user=user,
            price=price,
            title=title,
            content=content,
            status='Available',
            category=category
        )
        product.save()

        for f in files:
            image = Image(
                product=product,
                file=f
            )
            image.save()
        return HttpResponse(product.id)

    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def update_post(request, product_id):
    if request.method in ['POST', 'DELETE', 'GET']:
        product = Product.objects.filter(id=product_id)
        if not product.exists():
            return HttpResponseServerError('Product does not exist.')
        product = product[0]
        if request.method == 'GET':
            imgs = Image.objects.filter(product=product)
            img_urls = [img.file for img in imgs]
            response = {
                'id': product.id,
                'user': product.user.email,
                'time': product.time.strftime('%Y-%m-%d %H:%M'),
                'price': product.price,
                'status': product.status,
                'title': product.title,
                'content': product.content,
                'category': product.category,
                'images': img_urls
            }
            return HttpResponse(json.dumps(response, default=str))
        elif request.method == 'DELETE':
            product.delete()
            return HttpResponse('Delete successfully!')
        elif request.method == 'POST':
            files = request.FILES.getlist('img')
            product.price = request.POST.get('price')
            product.title = request.POST.get('title')
            product.content = request.POST.get('content')
            product.category = request.POST.get('category')
            product.save()
            Image.objects.filter(product=product).delete()
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, product_id), ignore_errors=True)
            for f in files:
                image = Image(
                    product=product,
                    file=f
                )
                image.save()
            return HttpResponse(product.id)
    else:
        return HttpResponseNotAllowed(['POST', 'DELETE'])


>>>>>>> dc11c7c6e52fc6476912a179dbb55bf55670ac0c
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
<<<<<<< HEAD
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
=======
        user = User(
            fname=fname,
            lname=lname,
            email=email,
            birthday=birthday,
            gender=gender,
            wat_id=wat_id,
            occupation=occ,
            phone=phone
        )
        user.save()

        pwd = Password(
            user=user,
            md5_pwd=password
        )
>>>>>>> dc11c7c6e52fc6476912a179dbb55bf55670ac0c
        pwd.save()

        return 1
    else:
        return 0
<<<<<<< HEAD

=======
>>>>>>> dc11c7c6e52fc6476912a179dbb55bf55670ac0c

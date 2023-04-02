import datetime

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.http import HttpResponseServerError, JsonResponse
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from backbone.models import User
from backbone.models import Password
from backbone.models import Product
from backbone.models import Image
from backbone.models import Order
from django.db.models import Q
import json
import shutil
import os
import jwt


def parse_token(header):
    auth_header = header.split()
    if len(auth_header) == 2 and auth_header[0] == 'Bearer':
        token = auth_header[1]
    else:
        token = auth_header[0]
    return token


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

        status = create_user(fname, lname, email, birthday, password,
                             gender, wat_id, occ, phone)
        if status == 1:
            return JsonResponse({
                'result': 'OK',
                'msg': 'User created successfully!'
            }
            )
        elif status == -1:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'Current email has already been registered.'
            }
            )
        else:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'Mandatory fields are empty.'
            }
            )
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
            return JsonResponse({
                'result': 'OK',
                'msg': 'Log in successfully',
                'data': {
                    'token': token
                }
            }
            )
        else:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'User does not exist or the password does not match'
            }
            )
    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        token = parse_token(request.META.get("HTTP_AUTHORIZATION"))

        files = request.FILES.getlist('img')
        email = request.POST.get("email")
        price = request.POST.get('price')
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        quality = request.POST.get('quality')

        user = get_object_or_404(User, email=email)
        token_cmp = Password.objects.get(user_id=email).token
        if token != token_cmp:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'Token does not match.'
            }
            )
        product = Product(
            user=user,
            price=price,
            title=title,
            content=content,
            status='Available',
            category=category,
            quality=quality
        )
        product.save()

        for f in files:
            image = Image(
                product=product,
                file=f
            )
            image.save()
        return JsonResponse(
            {
                'result': 'OK',
                'msg': 'Post created successfully!',
                'data': {
                    'productID': product.id
                }
            }
        )

    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def get_post(request):
    if request.method == 'GET':
        post_id = request.GET.get('id')
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        keyword = request.GET.get('keyword')

        filters = {}
        if post_id:
            filters['id'] = post_id
        if category:
            filters['category'] = category
        if min_price:
            filters['price__gte'] = min_price
        if max_price:
            filters['price__lte'] = max_price

        if keyword:
            products = Product.objects.filter(
                Q(title__contains=keyword) | Q(content__contains=keyword),
                **filters
            )
        else:
            products = Product.objects.filter(**filters)
        if not products.exists():
            return JsonResponse(
                {
                    'result': 'Failed',
                    'msg': 'Not found'
                }
            )

        res = []
        for product in products:
            imgs = Image.objects.filter(product=product)
            img_urls = [str(img.file) for img in imgs]
            data = {
                'id': product.id,
                'user': product.user.email,
                'time': product.time.strftime('%Y-%m-%d %H:%M'),
                'price': product.price,
                'status': product.status,
                'title': product.title,
                'content': product.content,
                'category': product.category,
                'quality': product.quality,
                'images': img_urls
            }
            res.append(data)
        return JsonResponse({
            'result': 'OK',
            'msg': 'Get successfully!',
            'data': {
                'postList': res
            }
        }
        )
    return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def get_my_post(request):
    if request.method == 'GET':
        token = parse_token(request.META.get("HTTP_AUTHORIZATION"))
        email = request.GET.get("email")
        token_cmp = get_object_or_404(Password, user_id=email).token
        if token != token_cmp:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'Token does not match.'
            }
            )
        products = Product.objects.filter(user_id=email)
        if not products.exists():
            return JsonResponse(
                {
                    'result': 'Failed',
                    'msg': 'Not found'
                }
            )
        res = []
        for product in products:
            imgs = Image.objects.filter(product=product)
            img_urls = [str(img.file) for img in imgs]
            data = {
                'id': product.id,
                'user': product.user.email,
                'time': product.time.strftime('%Y-%m-%d %H:%M'),
                'price': product.price,
                'status': product.status,
                'title': product.title,
                'content': product.content,
                'category': product.category,
                'quality': product.quality,
                'images': img_urls
            }
            res.append(data)
        return JsonResponse({
            'result': 'OK',
            'msg': 'Get successfully!',
            'data': {
                'postList': res
            }
        }
        )
    return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def update_post(request, product_id):
    if request.method in ['POST', 'DELETE']:
        product = get_object_or_404(Product, id=product_id)
        token = parse_token(request.META.get("HTTP_AUTHORIZATION"))
        email = product.user_id
        token_cmp = get_object_or_404(Password, user_id=email).token
        if token != token_cmp:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'Token does not match.'
            }
            )
        # delete a post
        # a problem is django cannot get any data from FE in DELETE method.
        if request.method == 'DELETE':
            product.delete()
            return JsonResponse({
                'result': 'OK',
                'msg': 'Delete successfully!',
            }
            )
        # update a post
        elif request.method == 'POST':
            files = request.FILES.getlist('img')
            product.price = request.POST.get('price')
            product.title = request.POST.get('title')
            product.content = request.POST.get('content')
            product.category = request.POST.get('category')
            product.quality = request.POST.get('quality')
            product.save()
            Image.objects.filter(product=product).delete()
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, product_id), ignore_errors=True)
            for f in files:
                image = Image(
                    product=product,
                    file=f
                )
                image.save()
            return JsonResponse({
                'result': 'OK',
                'msg': 'Update successfully!',
                'data': {
                    'productID': product.id
                }
            }
            )
    return HttpResponseNotAllowed(['POST', 'DELETE'])


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        token = parse_token(request.META.get("HTTP_AUTHORIZATION"))
        email = request.POST.get("email")

        buyer = get_object_or_404(User, email=email)
        seller_email = request.POST.get('seller')
        seller = get_object_or_404(User, email=seller_email)
        product_id = request.POST.get('product')
        product = get_object_or_404(Product, id=product_id)
        note = request.POST.get('note')

        token_cmp = Password.objects.get(user_id=email).token
        if token != token_cmp:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'Token does not match.'
            }
            )

        ordered = Product.objects.filter(id=product.id)
        if ordered:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'You have already placed this order!'
            }
            )

        order = Order(
            seller=seller,
            buyer=buyer,
            product=product,
            time=datetime.datetime.now(),
            status='Valid',
            note=note
        )
        order.save()
        product.status = "Pending"
        product.save()

        return JsonResponse(
            {
                'result': 'OK',
                'msg': 'Order created successfully!',
                'data': {
                    'orderID': order.id
                }
            }
        )

    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def get_my_order(request):
    if request.method == 'GET':
        token = parse_token(request.META.get("HTTP_AUTHORIZATION"))
        email = request.GET.get("email")
        token_cmp = get_object_or_404(Password, user_id=email).token
        if token != token_cmp:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'Token does not match.'
            }
            )
        orders_as_buyer = Order.objects.filter(buyer_id=email)
        orders_as_seller = Order.objects.filter(seller_id=email)
        if not orders_as_buyer.exists() and not orders_as_seller.exists():
            return JsonResponse(
                {
                    'result': 'Failed',
                    'msg': 'Not found'
                }
            )
        res = []
        for order in orders_as_buyer:
            product = get_object_or_404(Product, id=order.product_id)
            imgs = Image.objects.filter(product=product)
            img_urls = [str(img.file) for img in imgs]
            data = {
                'type': "buyer order",
                'id': order.id,
                'product': product.id,
                'title': product.title,
                'description': product.content,
                'price': product.price,
                'category': product.category,
                'quality': product.quality,
                'images': img_urls,
                'buyer': order.buyer_id,
                'seller': order.seller_id,
                'time': order.time,
                'status': order.status,
                'note': order.note
            }
            res.append(data)

        for order in orders_as_seller:
            product = get_object_or_404(Product, id=order.product_id)
            imgs = Image.objects.filter(product=product)
            img_urls = [str(img.file) for img in imgs]
            data = {
                'type': "seller order",
                'id': order.id,
                'product': product.id,
                'title': product.title,
                'description': product.content,
                'price': product.price,
                'category': product.category,
                'quality': product.quality,
                'images': img_urls,
                'buyer': order.buyer_id,
                'seller': order.seller_id,
                'time': order.time,
                'status': order.status,
                'note': order.note
            }
            res.append(data)
        return JsonResponse({
            'result': 'OK',
            'msg': 'Get successfully!',
            'data': {
                'orderList': res
            }
        }
        )
    return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def update_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        token = parse_token(request.META.get("HTTP_AUTHORIZATION"))
        email = order.buyer_id
        status = request.POST.get('status')

        token_cmp = Password.objects.get(user_id=email).token
        if token != token_cmp:
            return JsonResponse({
                'result': 'Failed',
                'msg': 'Token does not match.'
            }
            )

        order.status = status
        order.save()

        return JsonResponse(
            {
                'result': 'OK',
                'msg': 'Order cancelled successfully!',
                'data': {
                    'orderID': order.id
                }
            }
        )

    return HttpResponseNotAllowed(['POST'])


def create_user(fname, lname, email, birthday, password, gender, wat_id, occ, phone):
    if all([fname, lname, email, birthday, password]):
        if (User.objects.filter(email=email)):
            return -1
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
        pwd.save()

        return 1
    else:
        return 0

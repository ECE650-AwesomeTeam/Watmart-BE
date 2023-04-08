from django.test import TestCase, Client
from backbone.models import User
from backbone.models import Password
from backbone.models import Product
from backbone.models import Order 
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import json
from backbone.views import create_user

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            email='abc@abc.com',
            fname = 'xuan',
            lname = 'shi',
            birthday = '1888-08-08',
            gender = 'Male',
            wat_id = '21030179',
            occupation = 'Student',
            phone = '5485485488'
        )
    
    def test_create_user(self):
        user = User.objects.get(email='abc@abc.com')
        self.assertEqual(user.fname, 'xuan')
        self.assertEqual(user.gender, 'Male')
        self.assertEqual(user.phone, '5485485488')
    
    def test_update_user(self):
        user = User.objects.get(email='abc@abc.com')
        user.phone = '5485485477'
        self.assertEqual(user.fname, 'xuan')
        self.assertEqual(user.gender, 'Male')
        self.assertEqual(user.phone, '5485485477')


class PasswordTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            email='abc@abc.com',
            fname = 'xuan',
            lname = 'shi',
            birthday = '1888-08-08',
            gender = 'Male',
            wat_id = '21030179',
            occupation = 'Student',
            phone = '5485485488'
        )
        user = User.objects.get(email='abc@abc.com')
        Password.objects.create(user=user, md5_pwd='abc123abc')
    
    def test_fk(self):
        user = User.objects.get(email='abc@abc.com')
        pwd = Password.objects.get(user=user)
        self.assertNotEqual(pwd, None)
    
    def test_create_pwd(self):
        user = User.objects.get(email='abc@abc.com')
        pwd = Password.objects.get(user=user)
        self.assertEqual(pwd.md5_pwd, 'abc123abc')


class ProdcutTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            email='abc@abc.com',
            fname = 'xuan',
            lname = 'shi',
            birthday = '1888-08-08',
            gender = 'Male',
            wat_id = '21030179',
            occupation = 'Student',
            phone = '5485485488'
        )
        user = User.objects.get(email='abc@abc.com')
        Product.objects.create(
            user = user,
            price = 1.11,
            title = 'this is a test post.',
            content = 'Oh look! This is a test!',
            category = 'Books'
        )
    
    def test_fk(self):
        user = User.objects.get(email='abc@abc.com')
        product = Product.objects.get(user=user)
        self.assertNotEqual(product, None)
    
    def test_create_product(self):
        user = User.objects.get(email='abc@abc.com')
        product = Product.objects.get(user=user)
        self.assertEqual(product.price, 1.11)
        self.assertEqual(product.title, 'this is a test post.')
        self.assertEqual(product.category, 'Books')
    
    def test_product_id(self):
        user = User.objects.get(email='abc@abc.com')
        product = Product.objects.get(user=user)
        self.assertNotEqual(product.id, None)

class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_success(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'birthday': '2000-01-01',
            'password': 'secret',
            'gender': 'male',
            'watcardID': '12345',
            'occupation': 'student',
            'phone': '1234567890'
        }

        response = self.client.post('/signup', json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertEqual(response.json()['msg'], 'User created successfully!')

    def test_signup_email_already_registered(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'birthday': '2000-01-01',
            'password': 'secret',
            'gender': 'male',
            'watcardID': '12345',
            'occupation': 'student',
            'phone': '1234567890'
        }

        # Create a user with the same email before signing up
        create_user('Jane', 'Doe', 'johndoe@example.com', '2000-01-01', 'secret',
                    'female', '54321', 'student', '0987654321')

        response = self.client.post('/signup', json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'Current email has already been registered.')

    def test_signup_missing_mandatory_fields(self):
        data = {
            'firstName': '',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'birthday': '2000-01-01',
            'password': '',
            'gender': 'male',
            'watcardID': '',
            'occupation': 'student',
            'phone': ''
        }

        response = self.client.post('/signup', json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'Mandatory fields are empty.')


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@example.com',
            'birthday': '2000-01-01',
            'password': 'mypassword',
            'gender': 'male',
            'watcardID': '1234567890',
            'occupation': 'student',
            'phone': '1234567890'
        }

    def test_login_success(self):
        signup_response = self.client.post('/signup', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(signup_response.status_code, 200)

        # Login with the registered user
        login_data = {
            'email': 'johndoe@example.com',
            'password': 'mypassword'
        }
        response = self.client.post('/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json()['data'])

    def test_login_failure(self):
        # make a POST request to the login endpoint with invalid credentials
        response = self.client.post('/login', json.dumps(self.data), content_type='application/json')
        # check that the response has a 200 OK status code
        self.assertEqual(response.status_code, 200)
        # check that the response indicates login failure
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'User does not exist or the password does not match')


class CreatePostTestCase(TestCase):
    def setUp(self):
        # Sign up a test user
        signup_url = '/signup'
        signup_data = {
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'testuser@example.com',
            'birthday': '1990-01-01',
            'password': 'password',
            'gender': 'M',
            'watcardID': '1234567890',
            'occupation': 'Student',
            'phone': '123-456-7890',
        }
        response = self.client.post(signup_url, data=json.dumps(signup_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Log in and obtain a token
        login_url = '/login'
        login_data = {
            'email': 'testuser@example.com',
            'password': 'password'
        }
        response = self.client.post(login_url, data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.token = response.json()['data']['token']

    def test_create_post(self):
        url = '/post'
        data = {
            'img': '',
            'email': 'testuser@example.com',
            'price': '10.99',
            'title': 'Test Product',
            'content': 'This is a test product.',
            'category': 'Test',
            'quality': 'New'
        }
        response = self.client.post(url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertIsNotNone(Product.objects.filter(title='Test Product').first())


class GetPostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            fname='John',
            lname='Doe',
            email='test@test.com',
            birthday='2000-01-01',
            gender='Male',
            wat_id='1231231234',
            occupation='Student',
            phone='1231231234'
        )
        self.client = Client()
        self.product1 = Product.objects.create(
            user=self.user,
            price=10.99,
            title='Test Product 1',
            content='This is a test product.',
            category='Books',
            quality='New'
        )
        self.product2 = Product.objects.create(
            user=self.user,
            price=15.99,
            title='Test Product 2',
            content='This is another test product.',
            category='Sports',
            quality='Used'
        )

    def test_get_post_with_keyword(self):
        response = self.client.get('/post/?keyword=test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertEqual(len(response.json()['data']['postList']), 2)

    def test_get_post_with_category(self):
        response = self.client.get('/post/?category=Books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertEqual(len(response.json()['data']['postList']), 1)

    def test_get_post_with_price_range(self):
        response = self.client.get('/post/?min_price=10&max_price=12')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertEqual(len(response.json()['data']['postList']), 1)

    def test_get_post_with_id(self):
        response = self.client.get(f'/post/?id={self.product1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertEqual(len(response.json()['data']['postList']), 1)

    def test_get_post_not_found(self):
        response = self.client.get('/post/?keyword=none')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'Not found')


class GetMyPostTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email='testuser@example.com',
            fname='John',
            lname='Doe',
            birthday='2000-01-01',
            gender='Male',
            wat_id='1231231234',
            occupation='Student',
            phone='1231231234'
        )
        self.password = Password.objects.create(user=self.user, token='token')
        self.product1 = Product.objects.create(
            user=self.user,
            title='test title 1',
            content='test content 1',
            price=100.0,
            category='test category 1',
            quality='New',
            status='Sold',
        )
        self.product2 = Product.objects.create(
            user=self.user,
            title='test title 2',
            content='test content 2',
            price=200.0,
            category='test category 2',
            quality='New',
            status='Sold',
        )

    def test_get_my_post_success(self):
        email = 'testuser@example.com'
        token = 'token'
        response = self.client.get(
            f'/mypost/?email={email}', HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertEqual(len(response.json()['data']['postList']), 2)
        self.assertEqual(response.json()['data']['postList'][0]['title'], 'test title 1')
        self.assertEqual(response.json()['data']['postList'][1]['title'], 'test title 2')

    def test_get_my_post_invalid_token(self):
        email = 'testuser@example.com'
        token = 'invalid_token'
        response = self.client.get(
            f'/mypost/?email={email}', HTTP_AUTHORIZATION=f'Bearer {token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'Token does not match.')


class UpdatePostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email='testuser@example.com',
            fname='John',
            lname='Doe',
            birthday='2000-01-01',
            gender='Male',
            wat_id='1231231234',
            occupation='Student',
            phone='1231231234'
        )
        self.product = Product.objects.create(
            user_id="testuser@example.com",
            price="100",
            status="available",
            title="Test Product",
            content="This is a test product",
            category="test",
            quality="new"
        )
        self.password = Password.objects.create(
            user_id="testuser@example.com",
            token="testtoken"
        )
        self.url = f'/post/{self.product.id}'

    def test_update_post(self):
        # Send POST request to update post
        data = {
            'price': '200',
            'title': 'Updated Test Product',
            'content': 'This is an updated test product',
            'category': 'updatedtest',
            'quality': 'used'
        }
        response = self.client.post(
            self.url,
            data,
            format='multipart',
            HTTP_AUTHORIZATION=f'Bearer {self.password.token}'
        )

        # Check that the post was updated
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertEqual(response.json()['msg'], 'Update successfully!')
        self.assertEqual(response.json()['data']['productID'], self.product.id)

        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.title, data['title'])
        self.assertEqual(updated_product.content, data['content'])
        self.assertEqual(updated_product.category, data['category'])
        self.assertEqual(updated_product.quality, data['quality'])

    def test_delete_post(self):
        # Send DELETE request to delete post
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=f'Bearer {self.password.token}')

        # Check that the post was deleted
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertEqual(response.json()['msg'], 'Delete successfully!')
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_unauthorized(self):
        # Send POST request without token
        data = {
            'price': '200',
            'title': 'Updated Test Product',
            'content': 'This is an updated test product',
            'category': 'updatedtest',
            'quality': 'used'
        }
        response = self.client.post(
            self.url,
            data,
            format='multipart',
            HTTP_AUTHORIZATION='Bearer ???'
        )

        # Check that the request is unauthorized
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'Token does not match.')

        # Send DELETE request without token
        response = self.client.delete(self.url,
                                      HTTP_AUTHORIZATION='Bearer ???')

        # Check that the request is unauthorized
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'Token does not match.')


class CreateOrderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.buyer = User.objects.create(
            email='testbuyer@example.com',
            fname='John',
            lname='Doe',
            birthday='2000-01-01',
            gender='Male',
            wat_id='1231231234',
            occupation='Student',
            phone='1231231234'
        )
        self.seller = User.objects.create(
            email='testseller@example.com',
            fname='John',
            lname='Doe',
            birthday='2000-01-01',
            gender='Male',
            wat_id='1231231234',
            occupation='Student',
            phone='1231231234'
        )
        self.product = Product.objects.create(
            user=self.seller,
            price="100",
            status="available",
            title="Test Product",
            content="This is a test product",
            category="test",
            quality="new"
        )
        self.password = Password.objects.create(
            user=self.buyer,
            token="testtoken"
        )
        self.url = '/order'

    def test_create_order(self):
        # Send POST request to create order
        data = {
            'email': self.buyer.email,
            'seller': self.seller.email,
            'product': self.product.id,
            'note': 'This is a test order'
        }
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.password.token}'
        )

        # Check that the order was created
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'OK')
        self.assertEqual(response.json()['msg'], 'Order created successfully!')
        self.assertEqual(response.json()['data']['orderID'], Order.objects.latest('id').id)

        # Check that the product status was updated to "Pending"
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.status, "Pending")

        # Check that the order details are correct
        order = Order.objects.get(product=self.product)
        self.assertEqual(order.buyer, self.buyer)
        self.assertEqual(order.seller, self.seller)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.note, data['note'])

    def test_create_duplicate_order(self):
        # Create an order for the same product
        Order.objects.create(
            seller=self.seller,
            buyer=self.buyer,
            product=self.product,
            status='Valid'
        )

        # Send POST request to create order
        data = {
            'email': self.buyer.email,
            'seller': self.seller.email,
            'product': self.product.id,
            'note': 'This is a test order'
        }
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.password.token}'
        )

        # Check that the order was not created
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'You have already placed this order!')

    def test_unauthorized(self):
        # Send POST request without token
        data = {
            'email': self.buyer.email,
            'seller': self.seller.email,
            'product': self.product.id,
            'note': 'This is a test order'
        }
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer ???'
        )

        # Check that the request is unauthorized
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'Token does not match.')


class GetMyOrderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email='testuser@example.com',
            fname='John',
            lname='Doe',
            birthday='2000-01-01',
            gender='Male',
            wat_id='1231231234',
            occupation='Student',
            phone='1231231234'
        )
        self.password = Password.objects.create(
            user=self.user,
            token="testtoken"
        )
        self.token = self.password.token
        self.product = Product.objects.create(
            user_id = self.user.email,
            title='Test Product',
            content='Test Product Description',
            price=10.0,
            category='test category',
            quality='test quality'
        )

    def test_get_my_order_failed(self):
        url = '/myorder/?email=testuser@example.com'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.json().get('result'), 'Failed')
        self.assertEqual(response.json().get('msg'), 'Not found')

    def test_get_my_order(self):
        url = '/myorder/?email=testuser@example.com'
        self.order = Order.objects.create(
            buyer=self.user,
            seller=self.user,
            product=self.product,
            status='Valid',
            note='Test Order Note'
        )
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('data').get('orderList')), 2)
        order = response.json().get('data').get('orderList')[0]
        self.assertEqual(order.get('type'), 'buyer order')
        self.assertEqual(order.get('id'), self.order.id)
        self.assertEqual(order.get('product'), self.product.id)
        self.assertEqual(order.get('title'), self.product.title)
        self.assertEqual(order.get('description'), self.product.content)
        self.assertEqual(order.get('price'), self.product.price)
        self.assertEqual(order.get('category'), self.product.category)
        self.assertEqual(order.get('quality'), self.product.quality)
        self.assertEqual(order.get('buyer'), str(self.user.email))
        self.assertEqual(order.get('seller'), str(self.user.email))
        self.assertEqual(order.get('status'), self.order.status)
        self.assertEqual(order.get('note'), self.order.note)

    def test_get_my_order_unauthorized(self):
        url = '/myorder/?email=testuser@example.com'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer ???')
        self.assertEqual(response.json()['result'], 'Failed')
        self.assertEqual(response.json()['msg'], 'Token does not match.')


class TestUpdateOrder(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(
            email='user1@example.com',
            fname='John',
            lname='Doe',
            birthday='2000-01-01',
            gender='Male',
            wat_id='1231231234',
            occupation='Student',
            phone='1231231234'
        )
        self.user2 = User.objects.create(
            email='user2@example.com',
            fname='John',
            lname='Doe',
            birthday='2000-01-01',
            gender='Male',
            wat_id='1231231234',
            occupation='Student',
            phone='1231231234'
        )
        self.password1 = Password.objects.create(user=self.user1, token='token1')
        self.password2 = Password.objects.create(user=self.user2, token='token2')
        self.product = Product.objects.create(
            user_id=self.user1.email,
            title='product1', 
            content='content1', 
            price=10, 
            category='category1', 
            quality='new', 
            status='available')
        self.order = Order.objects.create(seller=self.user1, buyer=self.user2, product=self.product, time='2023-04-06 12:00:00', status='valid', note='note1')
        self.order_url = f'/order/{self.order.id}'

    def test_update_order(self):
        data = {'status': 'cancelled'}
        response = self.client.post(self.order_url, data, HTTP_AUTHORIZATION='Bearer token2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.get(id=self.order.id).status, 'cancelled')

    def test_update_order_with_invalid_token(self):
        data = {'status': 'cancelled'}
        response = self.client.post(self.order_url, data, HTTP_AUTHORIZATION='Bearer invalid_token')
        self.assertEqual(Order.objects.get(id=self.order.id).status, 'valid')
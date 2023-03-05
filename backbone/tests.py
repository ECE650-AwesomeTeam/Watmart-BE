from django.test import TestCase
from backbone.models import User
from backbone.models import Password
from backbone.models import Product

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


from rest_framework.test import APITestCase
from account.models import User


class TestModel(APITestCase):
    def test_create_user(self):
        user=User.objects.create_user(first_name='john', last_name='jeff',email='johnp20@gmail.com', password='test4321@john', phone='09050261635')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'johnp20@gmail.com')

   

    def test_raise_value_error_when_no_email(self):     
        self.assertRaises(ValueError,User.objects.create_user,first_name='john',last_name='jeff', email='',password='test4321@john',phone='08050261635')
    def test_raise_value_error_when_no_first_name(self):     
        self.assertRaises(ValueError,User.objects.create_user,first_name='',last_name='jeff', email='john24@gmail.com',password='test4321@john',phone='08050261635')

    def test_createsuper_user(self):
        user=User.objects.create_superuser(first_name='john', last_name='jeff', email='johnAdmin20@gmail.com', password='test4321@john', phone='08050261635')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_superuser_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(first_name='john', last_name='jeff',email='johnp20@gmail.com', password='test4321@john', phone='09050261635',is_staff=False)

    def test_superuser_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(first_name='john', last_name='jeff',email='johnp20@gmail.com', password='test4321@john', phone='09050261635',is_superuser=False)
    


    
        


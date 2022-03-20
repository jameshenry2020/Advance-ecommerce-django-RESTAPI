from rest_framework.test import APITestCase
from account.models import MyUser


class TestModel(APITestCase):
    def test_create_user(self):
        user=MyUser.objects.create_user(first_name='john', last_name='jeff', username='jeff2021',email='johnp20@gmail.com', password='test4321@john', phone='09050261635')
        self.assertIsInstance(user, MyUser)
        self.assertEqual(user.email, 'johnp20@gmail.com')

    def test_raise_value_error_when_no_username(self):     
        self.assertRaises(ValueError,MyUser.objects.create_user,first_name='john',last_name='jeff',username='', email='john21@gmail.com',password='test4321@john',phone='08050261635')

    def test_raise_value_error_with_message_when_no_username(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            MyUser.objects.create_user(first_name='john', last_name='jeff', username='',email='johnp20@gmail.com', password='test4321@john', phone='09050261635')
    
    def test_raise_value_error_when_no_email(self):     
        self.assertRaises(ValueError,MyUser.objects.create_user,first_name='john',last_name='jeff',username='james4321', email='',password='test4321@john',phone='08050261635')
    def test_raise_value_error_when_no_first_name(self):     
        self.assertRaises(ValueError,MyUser.objects.create_user,first_name='',last_name='jeff',username='testuser1', email='john24@gmail.com',password='test4321@john',phone='08050261635')

    def test_createsuper_user(self):
        user=MyUser.objects.create_superuser(first_name='john', last_name='jeff', username='admin2021',email='johnAdmin20@gmail.com', password='test4321@john', phone='08050261635')
        self.assertIsInstance(user, MyUser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_superuser_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            MyUser.objects.create_superuser(first_name='john', last_name='jeff', username='testuser22',email='johnp20@gmail.com', password='test4321@john', phone='09050261635',is_staff=False)

    def test_superuser_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            MyUser.objects.create_superuser(first_name='john', last_name='jeff', username='testuser22',email='johnp20@gmail.com', password='test4321@john', phone='09050261635',is_superuser=False)
    


    
        


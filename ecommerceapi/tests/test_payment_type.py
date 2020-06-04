
from django.test import TestCase
from ecommerceapi.models import Payment_Type, Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import datetime


class TestPaymentType(TestCase):

    def setUp(self):
        self.username = 'TestUser'
        self.password = 'Testing1234'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1, address="1234 Fake Street Nashville Tennessee", phone_number="123-4567")
        

    def test_post_payment_type(self):

        new_payment_type = {
            "merchant_name": "Mastercard",
            "account_number": "23343478347",
            "expiration_date": "2027-11-22",
            "created_at": datetime.datetime.now()
            
            }    
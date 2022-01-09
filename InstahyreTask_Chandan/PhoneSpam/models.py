from django.db import models
# Create your models here.
'''
Model for the Database
username,phone number and password are the required fields
Phonenumbers must be unique
password is used to register and create a account in database
spam is stored as False by default unless someone who is authenticated marks it as spam
'''
class Details(models.Model):
    username=models.CharField(blank=False,max_length=20)
    phone = models.IntegerField(blank=False,unique=True)
    email=models.EmailField(blank=True)
    password = models.CharField(blank=False, max_length=10)
    spam=models.BooleanField(default=False)


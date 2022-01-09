

from django.urls import path
from .views import register,markspam,allRegistered,allspam,knowUser
'''
    all urls are mentioned here with the appropriate classes
'''
urlpatterns = [
    path('register', register.as_view()),          #registering a user
    path('all', allRegistered.as_view()),          #display all users registered
    path('all/spam',allspam.as_view()),            #display all spam numbers
    path('markspam/<int:pk>',markspam.as_view()),  #mark a number as spam
    path('user',knowUser.as_view()),               #know a usernumber and spam status using name
]

from django.http import Http404
from rest_framework.views import APIView
from .serializers import details_serializers, passusername,all_details
from rest_framework.response import Response
from rest_framework import status
from .models import Details
from rest_framework.authentication import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

# Create your views here.

'''
    class allRegistered returns all the registered users stored in the database
    Methods supported : GET
    path : http://127.0.0.1:8000/all
    SessionAuthentication and BasicAuthentication is enabled
'''

class allRegistered(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Details.objects.all()
        serializer = details_serializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


'''
    class allspam is responsible for returning all the numbers and details of user which is marked as spam
    Methods supported : GET
    path : http://127.0.0.1:8000/all/spam
    SessionAuthentication and BasicAuthentication is enabled
'''

class allspam(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Details.objects.filter(spam=True)  # filtering objects based on spam
        serializer = details_serializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


'''
    class register is responsible for registering an user and saving the details in the database
    Methods supported : POST
    path : http://127.0.0.1:8000/register
    payload : { "name" : <string>name ,"phone" : <int>phone , "email" : <string>email(optional)  
        ,'password' :<password>}
    No authentication enabled as everyone can use this to register
    
    User should register using this API to access other functionalities/API's using basic auth
'''

class register(APIView):
    def post(self, request):
        data = all_details(data=request.data)
        if data.is_valid():  # check if the request data is valid
            data.save()
            username = data.data['username']
            password = data.data['password']
            email = data.data['email']
            user = User.objects.create_user(username=username,    #creates a user and stores it in the db
                                            email=email,
                                            password=password)
            return Response("Registered Successfully", status=status.HTTP_201_CREATED)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


'''
    class markspam is responsible for marking a registered number as spam
    Methods supported : GET ,PATCH
    path : http://127.0.0.1:8000/markspam/<phonenumber>
    
    PATCH is used to mark a number as spam
    payload : {"spam":true}
    SessionAuthentication and BasicAuthentication is enabled
    
    This can also be used to get the user details based on phone number
'''

class markspam(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def getobject(self, pk):
        try:
            return Details.objects.get(phone=pk)
        except Details.DoesNotExist:
            return Http404

    def get(self, request, pk):  # / /markspam/<phn number> to know the userdetails
        data = self.getobject(pk)
        serializer = details_serializers(data)
        return Response(serializer.data)

    def patch(self,request,pk):
        data=self.getobject(pk)
        serializer=details_serializers(data,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(f"{pk} Marked as spam")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
    class knowUser is responsible for returning the list of users matching the name with their phone number 
        and spam status
    Methods supported : POST
    path : http://127.0.0.1:8000/user
    payload : { "name" : <string>name }
    SessionAuthentication and BasicAuthentication is enabled
'''

class knowUser(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = passusername(data=request.data)
        if data.is_valid():
            username = data.data['username']
            lis = Details.objects.filter(username__iregex=rf'{username}')
            serializer = details_serializers(lis, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

from .models import Details
from rest_framework.serializers import ModelSerializer

'''This serializer is for requests which passes the all the fields'''
class all_details(ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'


'''This serializer is for requests which passes the all the fields except password'''
class details_serializers(ModelSerializer):
    class Meta:
        model = Details
        fields = ['username','phone','email','spam']


''' This serializer is for knowuser requests which only passes name parameter '''
class passusername(ModelSerializer):
    class Meta:
        model = Details
        fields = ['username']

from .models import Contact
from rest_framework import serializers
from django.contrib.auth.models import User

class contactserializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
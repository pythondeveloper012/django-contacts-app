import sys, os, django

# set the settings module manually
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
django.setup()

from contacts.models import Contact
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from contacts.serializers import contactserializer
from contacts.serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken







class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGetPostData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = Contact.objects.all()

        name = request.GET.get('name')
        phone = request.GET.get('phone')
        email = request.GET.get('email')

    # Apply filters if query params exist
        if name:
            users = users.filter(name__icontains=name)
        if phone:
            users = users.filter(phone__icontains=phone)
        if email:
            users = users.filter(email__icontains=email)

    # Serialize data
        serializer = contactserializer(users, many=True)

    # Return response
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = contactserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contact created Successfully!", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UsersUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_obj(self,  pk):
        try:
            users = Contact.objects.get(pk=pk)
            return users
        except:
            return None
        
    def get(self, request, pk):
        user = self.get_obj(pk)
        if not user:
            return Response({"Error": "Contact's ID Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = contactserializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        user = self.get_obj(pk)
        if user:
            user.delete()
            return Response({"Message": "Contact's Deleted Successfully!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Error": "Contact's ID Not Found!"}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk):
        item = self.get_obj(pk)
        if not item:
            return Response({"Error": "Contact With this ID Does't Exist!"}, status=status.HTTP_404_NOT_FOUND)
        data =request.data  
        item.name = data.get("name", item.name)
        item.phone = data.get("phone", item.phone)
        item.email= data.get("email", item.email)
        item.category = data.get("category", item.category)
        item.address = data.get("address", item.address)
        item.created_at = data.get("created_at", item.created_at)


        item.save()
        return Response({"message": "Item updated successfully!"})

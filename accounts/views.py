from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

# Create your views here.

class CreateAdminOnce(APIView):
    def get(self, request):
        if User.objects.filter(username='admin').exists():
            return Response({'message': 'Admin user already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        User.objects.create_superuser(username='admin', password='admin123')
        return Response({'message': 'Admin user created successfully'}, status=status.HTTP_201_CREATED)

class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password','email'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
            },
        ),
        responses={
            201: openapi.Response(description='User registered successfully'),
            400: openapi.Response(description='Bad request')
        }
    )
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        email=request.data.get('email')
        if not username or not password :
            return Response({'error':'Username and password are required'},status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({'error':'Username already exists'},status=400) 
        User.objects.create_user(username=username,password=password,email=email)
        return Response({'message':'User registered successfully'},status=201)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

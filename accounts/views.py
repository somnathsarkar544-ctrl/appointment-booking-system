from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import status

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        email=request.data.get('email')
        if not username or not password :
            return Response({'error':'Username and password are required'},status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({'error':'Username already exists'},status=400) 
        user = User.objects.create_user(username=username,password=password,email=email)
        return Response({'message':'User registered successfully'},status=201)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

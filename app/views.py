from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import Chat
from .serializers import UserSerializer
from .models import User


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_chat(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Token '):
        return Response({"error": "Token is missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)
    token_key = auth_header.split(' ')[1]
    try:
        token = Token.objects.get(key=token_key)
        profile = token.user
        if profile.tokens>= 100:
            profile.tokens -= 100
            profile.save()
            response_data = {
                "message": "This is a Sample response from System",
            
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Insufficient tokens"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def token_balance(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Token '):
        return Response({"error": "Token is missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)
    token_key = auth_header.split(' ')[1]
    try:
        token = Token.objects.get(key=token_key)
        profile = token.user
        
        response_data = {
                
                "remaining_tokens": profile.tokens
            }
        return Response(response_data, status=status.HTTP_200_OK)    
        
    except User.DoesNotExist:
        return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
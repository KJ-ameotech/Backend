from django.contrib.auth import authenticate, login
from rest_framework import status, viewsets, permissions
from rest_framework import generics
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
import numpy as np
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile,Preference, UserLike, UploadedImages, Subscription,CustomUser
from .serializers import CustomUserSerializer, ProfileSerializer, PreferenceSerializer, UserLikeSerializer, UploadedImagesSerializer, SubscriptionSerializer
import cv2
from django.views.decorators.csrf import csrf_exempt
class CustomUserRegistration(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')

        if CustomUser.objects.filter(username=username).exists():
            response_data = {"error": "Username address already in use."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            response_data = {"error": "Email address already in use."}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            response_data = "Welcome you account is successfullly registered"
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        liked_user_id = request.data.get('liked_user_id')

        if liked_user_id == request.user.id:
            return Response({'detail': 'You cannot like yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already liked the same user before
        if UserLike.objects.filter(user=request.user, liked_user_id=liked_user_id).exists():
            return Response({'detail': 'You already liked this user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has an active subscription
        user_subscription = Subscription.objects.filter(user=request.user, end_date__gte=timezone.now()).first()
        if not user_subscription:
            return Response({'detail': 'Please upgrade your plan.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the like
        like = UserLike.objects.create(user=request.user, liked_user_id=liked_user_id)

        # Check if there is a mutual like
        if UserLike.objects.filter(user=like.liked_user, liked_user=request.user).exists():
            # Send an email notification about the match
            print("Congratulations! It's a match!")

        serializer = UserLikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserLogin(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)

            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            response_data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # If authentication fails, return an error response
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        # Ensure the serializer receives the image data
        uploaded_image = self.request.FILES.get('profile_picture')

        # Check if the uploaded image contains a human face
        if not self.contains_human_face(uploaded_image):
            return Response({'error': 'Please provide an image with a single human face.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(profile_picture=uploaded_image)

    def contains_human_face(self, image):
        # Load the Haar Cascade Classifier for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Read the uploaded image
        image_data = image.read()
        nparr = np.fromstring(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # Check if only one face is found
        if len(faces) == 1:
            return True
        else:
            return False


class UploadedImagesListCreateView(generics.ListCreateAPIView):
    queryset = UploadedImages.objects.all()
    serializer_class = UploadedImagesSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UploadedImagesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UploadedImages.objects.all()
    serializer_class = UploadedImagesSerializer

class PreferenceListCreateView(generics.ListCreateAPIView):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer

class PreferenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer

class SubscriptionAPIView(APIView):
    def get(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
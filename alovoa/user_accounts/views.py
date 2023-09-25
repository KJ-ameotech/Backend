from django.contrib.auth import authenticate, login
from rest_framework import status, viewsets, permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.http import JsonResponse
import numpy as np
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .models import Profile,Preference, UserLike, UploadedImages,Religion, Subscription,CustomUser, Community,State,District
from .serializers import (CustomUserSerializer, ProfileSerializer,
                          PreferenceSerializer, UserLikeSerializer,
                          UploadedImagesSerializer, SubscriptionSerializer,
                          CommunitySerializer,ReligionSerializer,StateSerializer,
                          DistrictSerializer)
import cv2
from django.views.decorators.csrf import csrf_exempt
class CustomUserRegistration(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')

        if CustomUser.objects.filter(username=username).exists():
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'error': 'Username address already in use.'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'error': 'Email address already in use.'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                'status_code': status.HTTP_201_CREATED,
                'message': 'Welcome, your account is successfully registered.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'errors': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class CustomUserDetailView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'  # or 'pk' depending on how you want to identify users

class CustomUserUpdateView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'  # or 'pk' depending on how you want to identify users

class CustomUserDeleteView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'id'  # or 'pk' depending on how you want to identify users
class UserLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        liked_user_id = request.data.get('liked_user_id')

        if liked_user_id == request.user.id:
            return Response({'detail': 'You cannot like yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already liked the same user before
        if UserLike.objects.filter(user=request.user, liked_user_id=liked_user_id).exists():
            return Response({'detail': 'You already liked this user.'}, status=status.HTTP_400_BAD_REQUEST)

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
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if email is not None:
            try:
                user = CustomUser.objects.get(email=email)
                
            except CustomUser.DoesNotExist:
                user = None
            userdata = CustomUser.objects.get(email=email)
            user_id = userdata.id
            
            if user is not None:
                # Authenticate the user using email
                if user.check_password(password):
                    # Password matches, log the user in
                    login(request, user)

                    # Generate refresh and access tokens
                    refresh = RefreshToken.for_user(user)
                    response_data = {
                        'status_code': status.HTTP_200_OK,
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'user_id': user_id
                        
                        
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    # If authentication fails, return an error response
                    response_data = {
                        'status_code': status.HTTP_401_UNAUTHORIZED,
                        'detail': 'Invalid credentials',
                    }
                    return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # If user not found, return an error response
                response_data = {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'detail': 'User not found',
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        else:
        # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # If authentication is successful, log the user in
                login(request, user)

                # Generate refresh and access tokens
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'status_code': status.HTTP_200_OK,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # If authentication fails, return an error response
                response_data = {
                    'status_code': status.HTTP_401_UNAUTHORIZED,
                    'detail': 'Invalid credentials',
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
class UserLoginWithEmail(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Try to find the user by email
        try:
            user = CustomUser.objects.get(email=email)
            
        except CustomUser.DoesNotExist:
            user = None
        userdata = CustomUser.objects.get(email=email)
        user_id = userdata.id
        
        if user is not None:
            # Authenticate the user using email
            if user.check_password(password):
                # Password matches, log the user in
                login(request, user)

                # Generate refresh and access tokens
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'status_code': status.HTTP_200_OK,
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_id': user_id
                    
                    
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # If authentication fails, return an error response
                response_data = {
                    'status_code': status.HTTP_401_UNAUTHORIZED,
                    'detail': 'Invalid credentials',
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # If user not found, return an error response
            response_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'detail': 'User not found',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)






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

        # Check if exactly one face is found
        if len(faces) == 1:
            return True
        else:
            return False
        
class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UploadedImagesListCreateView(generics.ListCreateAPIView):
    queryset = UploadedImages.objects.all()
    serializer_class = UploadedImagesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the uploaded images and get the created instances
        uploaded_images = serializer.save()

        # Construct a custom response with details about the created images
        response_data = {
            "message": "Images uploaded successfully.",
            "images": UploadedImagesSerializer(uploaded_images, many=True).data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




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


class CommunityList(APIView):
    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommunityDetail(APIView):
    def get_object(self, pk):
        try:
            return Community.objects.get(pk=pk)
        except Community.DoesNotExist:
            return None

    def get(self, request, pk):
        community = self.get_object(pk)
        if community is not None:
            serializer = CommunitySerializer(community)
            return Response(serializer.data)
        return Response({'detail': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        community = self.get_object(pk)
        if community is not None:
            serializer = CommunitySerializer(community, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        community = self.get_object(pk)
        if community is not None:
            community.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)



class ReligionList(APIView):
    def get(self, request):
        religions = Religion.objects.all()
        serializer = ReligionSerializer(religions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReligionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReligionDetail(APIView):
    def get_object(self, pk):
        try:
            return Religion.objects.get(pk=pk)
        except Religion.DoesNotExist:
            return None

    def get(self, request, pk):
        religion = self.get_object(pk)
        if religion is not None:
            serializer = ReligionSerializer(religion)
            return Response(serializer.data)
        return Response({'detail': 'Religion not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        religion = self.get_object(pk)
        if religion is not None:
            serializer = ReligionSerializer(religion, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Religion not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        religion = self.get_object(pk)
        if religion is not None:
            religion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Religion not found'}, status=status.HTTP_404_NOT_FOUND)

class CommunityByReligionBy(APIView):
    def get(self, request, religion_id):
        try:
            # Filter religions by religion's ID
            religion = Religion.objects.get(id=religion_id)
            communities = Community.objects.filter(religion=religion)
            serializer = ReligionSerializer(communities, many=True)  # Use 'communities' here, not 'religions'
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Religion.DoesNotExist:
            return Response({'detail': 'Religion not found'}, status=status.HTTP_404_NOT_FOUND)


class StateList(APIView):
    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StateDetail(APIView):
    def get_object(self, pk):
        try:
            return State.objects.get(pk=pk)
        except State.DoesNotExist:
            return None

    def get(self, request, pk):
        state = self.get_object(pk)
        if state is not None:
            serializer = StateSerializer(state)
            return Response(serializer.data)
        return Response({'detail': 'State not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        state = self.get_object(pk)
        if state is not None:
            serializer = StateSerializer(state, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'State not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        state = self.get_object(pk)
        if state is not None:
            state.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'State not found'}, status=status.HTTP_404_NOT_FOUND)


class DistrictList(APIView):
    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictSerializer(districts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DistrictSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DistrictDetail(APIView):
    def get_object(self, pk):
        try:
            return District.objects.get(pk=pk)
        except District.DoesNotExist:
            return None

    def get(self, request, pk):
        district = self.get_object(pk)
        if district is not None:
            serializer = DistrictSerializer(district)
            return Response(serializer.data)
        return Response({'detail': 'District not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        district = self.get_object(pk)
        if district is not None:
            serializer = DistrictSerializer(district, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'District not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        district = self.get_object(pk)
        if district is not None:
            district.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'District not found'}, status=status.HTTP_404_NOT_FOUND)


class DistrictsByState(APIView):
    def get(self, request, state_id):
        try:
            # Perform a lookup by state ID
            state = State.objects.get(id=state_id)

            # Filter districts by the retrieved state
            districts = District.objects.filter(state=state)
            serializer = DistrictSerializer(districts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except State.DoesNotExist:
            return Response({'detail': 'State not found'}, status=status.HTTP_404_NOT_FOUND)



class CheckEmailExists(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        # Check if the email exists in the database
        User = CustomUser
        try:
            user = User.objects.get(email=email)

            # Update the user's password
            # user.set_password(new_password)
            # user.save()

            return Response({'message': 'Email found',"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'exists': False, "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        
class ChangePassword(APIView):
    pass
    # def post(self, request):
    #     email = request.data.get('email')
    #     new_password = request.data.get('new_password')

    #     # Check if the email exists in the database
    #     User = CustomUser
    #     try:
    #         user = User.objects.get(email=email)

    #         # Update the user's password
    #         user.set_password(new_password)
    #         user.save()

    #         return Response({'message': 'Password Changed successfully',"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)
    #     except User.DoesNotExist:
    #         return Response({'Error while changing password': False, "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)Screenshot from 2023-09-20 18-17-40
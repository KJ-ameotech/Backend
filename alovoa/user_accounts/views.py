from django.contrib.auth import authenticate, login
from rest_framework import status, viewsets, permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.http import JsonResponse
import numpy as np
from django.http import Http404
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .models import Profile,Preference, UserLike, UploadedImages,Religion, ProfilePicture,Subscription,CustomUser, Community,State,District
from .serializers import (CustomUserSerializer, ProfileSerializer,
                          PreferenceSerializer, UserLikeSerializer,
                          UploadedImagesSerializer, SubscriptionSerializer,
                          CommunitySerializer,ReligionSerializer,StateSerializer,
                          DistrictSerializer, ProfilePictureSerializer)
import cv2
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings

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


class UserLikeListCreateView(generics.ListCreateAPIView):
    queryset = UserLike.objects.all()
    serializer_class = UserLikeSerializer



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if 'user' and 'liked_user' exist in the database
        user_id = serializer.validated_data['user'].id
        liked_user_id = serializer.validated_data['liked_user'].id

        user_exists = CustomUser.objects.filter(id=user_id).exists()
        liked_user_exists = CustomUser.objects.filter(id=liked_user_id).exists()

        if not user_exists or not liked_user_exists:
            return Response({'error': 'User or liked user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserLike.objects.all()
    serializer_class = UserLikeSerializer


    def get(self, request, *args, **kwargs):
        try:
            user_like = self.get_object()
            serializer = self.get_serializer(user_like)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserLike.DoesNotExist:
            return Response({'error': 'UserLike does not exist.'}, status=status.HTTP_404_NOT_FOUND)

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
            userdata = CustomUser.objects.get(username=username)
            user_id = userdata.id

            if user is not None:
                # If authentication is successful, log the user in
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



class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()    
    serializer_class = ProfileSerializer




class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'

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

class SubscriptionListAPIView(APIView):
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

class SubscriptionDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Subscription.objects.get(pk=pk)
        except Subscription.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        subscription = self.get_object(pk)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def put(self, request, pk):
        subscription = self.get_object(pk)
        serializer = SubscriptionSerializer(subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subscription = self.get_object(pk)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class UserProfilepictureListCreateView(generics.ListCreateAPIView):
    queryset = ProfilePicture.objects.all()
    serializer_class = ProfilePictureSerializer

class UserProfilepictureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfilePicture.objects.all()
    serializer_class = ProfilePictureSerializer
    lookup_field = 'user_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['status_code'] = status.HTTP_200_OK  # Include the status code in the response
        return Response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['status_code'] = status.HTTP_200_OK  # Include the status code in the response
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CheckEmailExists(APIView):
    def post(self, request):
        email = request.data.get('email')
        User = CustomUser
        try:
            user = User.objects.get(email=email)
            return Response({'message': 'Email found',"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'exists': False, "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        
class ChangePassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        print(email, new_password)
        # Check if the email exists in the database
        User = CustomUser
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password Changed successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

from django.utils import timezone
from django.db.models import Q


class CustomUserSearchAPIView(APIView):
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        # Get parameters from the request
        age_from = self.request.query_params.get('age_from')
        age_to = self.request.query_params.get('age_to')
        gender = self.request.query_params.get('gender')
        religion = self.request.query_params.get('religion')

        # Start with all users
        queryset = CustomUser.objects.all()

        # Create dictionaries to store profile pictures and profile data
        profile_images = {}
        profile_data_dict = {}

        for user in queryset:
            user_id = user.id

            # Fetch profile picture for the user if available
            profile_image = ProfilePicture.objects.filter(user_id=user_id).first()
            if profile_image:
                profile_images[user_id] = profile_image.image.url
            else:
                profile_images[user_id] = None

            # Fetch profile data for the user if available
            profile_data = Profile.objects.filter(user_id=user_id).first()
            if profile_data:
                # Assuming you have a UserProfileSerializer for the profile data
                profile_data_serializer = ProfileSerializer(profile_data)
                profile_data_dict[user_id] = profile_data_serializer.data
            else:
                profile_data_dict[user_id] = None

        # Filter by age (assuming date_of_birth is in yyyy-mm-dd format)
        if age_from and age_to:
            birth_year_to = timezone.now().year - int(age_from)
            birth_year_from = timezone.now().year - int(age_to)
            queryset = queryset.filter(
                Q(date_of_birth__year__lte=birth_year_to) &
                Q(date_of_birth__year__gte=birth_year_from)
            )

        # Filter by gender
        if gender:
            queryset = queryset.filter(gender=gender)

        # Filter by religion
        if religion:
            queryset = queryset.filter(religion=religion)

        # Serialize the queryset
        serializer = self.serializer_class(queryset, many=True)

        # Add profile_images and profile_data to the serialized data
        for user_data in serializer.data:
            user_id = user_data['id']
            user_data['profile_picture'] = profile_images.get(user_id)
            user_data['profile_data'] = profile_data_dict.get(user_id)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLikeAPIView(APIView):
    serializer_class = UserLikeSerializer  # Replace with your actual serializer

    def get(self, request, *args, **kwargs):
        # Get the liked_user_id from the URL query parameter
        liked_user_id = self.request.query_params.get('liked_user_id')

        # Check if liked_user_id is provided in the query parameters
        if liked_user_id is not None:
            # Filter UserLike objects based on the liked_user_id
            queryset = UserLike.objects.filter(liked_user_id=liked_user_id)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If liked_user_id is not provided, return a 400 Bad Request response
            return Response({"error": "liked_user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

class UserLikeCountAPIView(APIView):
    serializer_class = UserLikeSerializer  # Replace with your actual serializer

    def get(self, request, *args, **kwargs):
        # Get the liked_user_id from the URL query parameter
        liked_user_id = self.request.query_params.get('liked_user_id')
        # Check if liked_user_id is provided in the query parameters
        if liked_user_id is not None:
            # Filter UserLike objects based on the liked_user_id and get the count
            count = UserLike.objects.filter(liked_user_id=liked_user_id).count()
            return Response({"count": count}, status=status.HTTP_200_OK)
        else:
            # If liked_user_id is not provided, return a 400 Bad Request response
            return Response({"error": "liked_user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
class CustomUserList(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        user_serializer = CustomUserSerializer(users, many=True)

        user_data_with_images_and_profile = []

        for user in user_serializer.data:
            user_data = user  # Copy the user data to a new dictionary
            # Get the user's profile picture if available
            try:
                profile_picture = ProfilePicture.objects.get(user=user['id'])
                profile_picture_serializer = ProfilePictureSerializer(profile_picture)
                user_data['profile_picture'] = profile_picture_serializer.data
            except ProfilePicture.DoesNotExist:
                user_data['profile_picture'] = None  # No profile picture found
            # Get the user's profile data if available
            try:
                profile_data = Profile.objects.get(user=user['id'])  # Assuming UserProfile is your profile model
                profile_data_serializer = ProfileSerializer(profile_data)  # Create a serializer for UserProfile
                user_data['profile_data'] = profile_data_serializer.data
            except Profile.DoesNotExist:
                user_data['profile_data'] = None  # No profile data found
            user_data_with_images_and_profile.append(user_data)
        return Response(user_data_with_images_and_profile)


class UserLikeListViewRequestsAccepted(APIView):
    def get(self, request, user_id):
        user_likes = UserLike.objects.filter(user_id=user_id, approved=True)
        liked_user_ids = [user_like.liked_user.id for user_like in user_likes]
        user_data = CustomUser.objects.filter(id=user_id)
        liked_users_data = CustomUser.objects.filter(id__in=liked_user_ids)
        profile_data = Profile.objects.filter(user_id__in=[user_id] + liked_user_ids)
        profile_picture_data = ProfilePicture.objects.filter(user_id__in=[user_id] + liked_user_ids)
        user_likes_data = UserLikeSerializer(user_likes, many=True).data
        user_data = CustomUserSerializer(user_data, many=True).data
        liked_users_data = CustomUserSerializer(liked_users_data, many=True).data
        profile_data = ProfileSerializer(profile_data, many=True).data
        profile_picture_data = ProfilePictureSerializer(profile_picture_data, many=True).data
        user_data_dict = {user['id']: user for user in user_data}
        liked_users_data_dict = {user['id']: user for user in liked_users_data}
        # profile_data_dict = {profile['user']: profile for profile in profile_data}
        profile_picture_data_dict = {picture['user']: picture for picture in profile_picture_data}

        merged_data = []

        for user_like in user_likes_data:
            user_id = user_like['user']
            liked_user_id = user_like['liked_user']
            user_data_entry = user_data_dict.get(user_id)
            liked_user_data_entry = liked_users_data_dict.get(liked_user_id)
            # profile_data_entry = profile_data_dict.get(user_id)
            user_profile_picture_data_entry = profile_picture_data_dict.get(user_id)
            liked_user_profile_picture_data_entry = profile_picture_data_dict.get(liked_user_id)

            if user_data_entry:
                merged_entry = {**user_like, 'user_data': user_data_entry}

                if liked_user_data_entry:
                    merged_entry['liked_user_data'] = liked_user_data_entry

                # if profile_data_entry:
                #     merged_entry['profile_data'] = profile_data_entry

                if user_profile_picture_data_entry:
                    merged_entry['user_profile_picture_data'] = user_profile_picture_data_entry

                if liked_user_profile_picture_data_entry:
                    merged_entry['liked_user_profile_picture_data'] = liked_user_profile_picture_data_entry

                merged_data.append(merged_entry)

        return Response(merged_data, status=status.HTTP_200_OK)



class LikedUserLikeListViewRequestsAccepted(APIView):
    def get(self, request, liked_user_id):
        # Retrieve UserLike objects where the specified user is liked (liked_user) with approved=True
        user_likes = UserLike.objects.filter(liked_user_id=liked_user_id, approved=True)
        liked_user  = UserLike.objects.filter(user=liked_user_id, approved=True)

        # Extract user IDs who liked the specified user
        user_ids = [user_like.user.id for user_like in user_likes]
        like_user_ids = [c_user.liked_user.id for c_user in liked_user]

        user_ids = user_ids + like_user_ids

        user_data = CustomUser.objects.filter(id__in=user_ids)

        user_data = CustomUserSerializer(user_data, many=True).data

        profile_images = ProfilePicture.objects.filter(user__id__in=user_ids)
        profile_images_data = ProfilePictureSerializer(profile_images, many=True).data

        for user, profile_image_data in zip(user_data, profile_images_data):
            slugList = user_likes.filter(user = user['id'])
            if not slugList:
                slugList = liked_user.filter(liked_user = user['id'])

            user['profile_image'] = profile_image_data['image']
            user['slug'] = slugList[0].slug

        return Response(user_data, status=status.HTTP_200_OK)


class ProfileSearchView(APIView):
    def get(self, request):
        # Get query parameters
        start_height = self.request.query_params.get('startheight')
        end_height = self.request.query_params.get('endheight')
        caste = self.request.query_params.get('caste')
        marital_status = self.request.query_params.get('marital_status')
        min_weight = self.request.query_params.get('minweight')
        max_weight = self.request.query_params.get('maxweight')
        min_income = self.request.query_params.get('minincome')
        max_income = self.request.query_params.get('maxincome')
        skin_tone = self.request.query_params.get('skin_tone')

        # Build the query for filtering profiles
        query_params = {}

        if start_height and end_height:
            query_params['height__gte'] = start_height
            query_params['height__lte'] = end_height

        if caste:
            query_params['caste'] = caste

        if marital_status:
            query_params['marital_status'] = marital_status

        if min_weight and max_weight:
            query_params['weight__gte'] = min_weight
            query_params['weight__lte'] = max_weight

        if min_income and max_income:
            query_params['income__gte'] = min_income
            query_params['income__lte'] = max_income

        if skin_tone:
            query_params['skin_tone'] = skin_tone

        # Execute the query and retrieve matching profiles
        matching_profiles = Profile.objects.filter(**query_params)
        serializer = ProfileSerializer(matching_profiles, many=True)

        return Response({'results': serializer.data})


class CustomUserUpdateAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')  # assuming you have a URL parameter for the user's ID
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# ________________________________________________________________________________________________________________**************************************___________________________________________________________________________

stripe.api_key = settings.STRIPE_SECRET_KEY
class StripePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Retrieve the amount from the request data or adapt as needed
            amount = request.data.get('amount', 1000)  # Amount in cents (e.g., $10.00)
            currency = 'usd'  # Change to your desired currency code

            # Create a Stripe Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency
            )

            return Response({'client_secret': intent.client_secret}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

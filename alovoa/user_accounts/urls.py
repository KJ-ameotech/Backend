from django.urls import path
from .views import (CustomUserRegistration, UserLogin,
                    ProfileListCreateView, ProfileDetailView,PreferenceListCreateView,
                    PreferenceDetailView, UserLikeAPIView,UploadedImagesListCreateView,
                    SubscriptionAPIView,UserLoginWithEmail,CommunityList, CommunityDetail
                    ,ReligionList,ReligionDetail,ReligionByCommunity)



urlpatterns = [
    path('register/', CustomUserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('email/login/', UserLoginWithEmail.as_view(), name='email-login'),
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('preferences/', PreferenceListCreateView.as_view(), name='preference-list-create'),
    path('preferences/<int:pk>/', PreferenceDetailView.as_view(), name='preference-detail'),
    path('like/', UserLikeAPIView.as_view(), name='user-like'),
    path('uploaded_images/', UploadedImagesListCreateView.as_view(), name='image-upload'),
    path('subcription/', SubscriptionAPIView.as_view(), name='subcription'),
    path('communities/', CommunityList.as_view(), name='community-list'),
    path('communities/<int:pk>/', CommunityDetail.as_view(), name='community-detail'),
    path('religions/', ReligionList.as_view(), name='religion-list'),
    path('religions/<int:pk>/', ReligionDetail.as_view(), name='religion-detail'),
    path('community/<str:community_name>/religions/', ReligionByCommunity.as_view(), name='religions-by-community'),
]

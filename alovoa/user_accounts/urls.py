from django.urls import path
from .views import (CustomUserRegistration, UserLogin,
                    ProfileListCreateView, ProfileDetailView,PreferenceListCreateView,
                    PreferenceDetailView, UserLikeAPIView,UploadedImagesListCreateView,
                    SubscriptionAPIView,UserLoginWithEmail,CommunityList, CommunityDetail
                    ,ReligionList,ReligionDetail,CommunityByReligionBy,StateList,StateDetail,
                    DistrictList,DistrictDetail,DistrictsByState,CheckEmailExists,
                    ChangePassword, CustomUserDetailView, CustomUserUpdateView, CustomUserDeleteView)





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
    path('community/<int:religion_id>/religions/', CommunityByReligionBy.as_view(), name='religions-by-community'),
    path('states/', StateList.as_view(), name='state-list'),
    path('states/<int:state_id>/', StateDetail.as_view(), name='state-detail'),
    path('districts/', DistrictList.as_view(), name='district-list'),
    path('districts/<int:pk>/', DistrictDetail.as_view(), name='district-detail'),
    path('districts/<str:state_name>/', DistrictsByState.as_view(), name='districts-by-state'),
    path('forget-password/', CheckEmailExists.as_view(), name='check-email-exists'),
    path('password-change/', ChangePassword.as_view(), name='change-password'),
    path('api/user/<int:id>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('api/user/<int:id>/update/', CustomUserUpdateView.as_view(), name='user-update'),
    path('api/user/<int:id>/delete/', CustomUserDeleteView.as_view(), name='user-delete'),
]

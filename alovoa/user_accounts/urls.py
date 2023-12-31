from django.urls import path
from .views import *





urlpatterns = [
    path('register/', CustomUserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('preferences/', PreferenceListCreateView.as_view(), name='preference-list-create'),
    path('preferences/<int:pk>/', PreferenceDetailView.as_view(), name='preference-detail'),
    path('like/', UserLikeListCreateView.as_view(), name='user-like'),
    path('uploaded_images/', UploadedImagesListCreateView.as_view(), name='image-upload'),
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>/', SubscriptionDetailAPIView.as_view(), name='subscription-detail'),
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
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list'),
    path('profiles/<int:user>/', ProfileRetrieveUpdateDestroyView.as_view(), name='profile-detail'),
    path('api/user/<int:id>/delete/', CustomUserDeleteView.as_view(), name='user-delete'),
    path('profiles_picture/', UserProfilepictureListCreateView.as_view(), name='profile-list-create'),
    path('profiles_picture/<int:user_id>/', UserProfilepictureDetailView.as_view(), name='profile-detail'),
    path('search/', CustomUserSearchAPIView.as_view(), name='user-search'),
    path('userlikes/<int:pk>/', UserLikeDetailView.as_view(), name='userlike-detail'),
    path('api/notification/', UserLikeAPIView.as_view(), name='follow-notification'),
    path('api/all-users/', CustomUserList.as_view(), name='all-users'),
    path('api/notification-count/', UserLikeCountAPIView.as_view(), name='count'),
    path('followed-users/<int:user_id>/', UserLikeListViewRequestsAccepted.as_view(), name='user-like-list'),
    path('liked-users-likes/<int:liked_user_id>/', LikedUserLikeListViewRequestsAccepted.as_view(), name='liked-users-likes'),
    path('api/profile/advanced/search/', ProfileSearchView.as_view(), name='profile-search'),
    path('users/<int:pk>/patch', CustomUserUpdateAPIView.as_view(), name='customuser-update'),
    path('stripe/payment/', StripePaymentView.as_view(), name='stripe-payment'),
    path('user-likerequest/', UserLikeRequestListView.as_view(), name='user-like-list'),

]

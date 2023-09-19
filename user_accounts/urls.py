from django.urls import path
from .views import CustomUserRegistration, UserLogin,ProfileListCreateView, ProfileDetailView,PreferenceListCreateView, PreferenceDetailView, UserLikeAPIView,UploadedImagesListCreateView, SubscriptionAPIView, UploadedImagesRetrieveUpdateDestroyView



urlpatterns = [
    path('register/', CustomUserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('preferences/', PreferenceListCreateView.as_view(), name='preference-list-create'),
    path('preferences/<int:pk>/', PreferenceDetailView.as_view(), name='preference-detail'),
    path('like/', UserLikeAPIView.as_view(), name='user-like'),
    path('uploaded_images/', UploadedImagesListCreateView.as_view(), name='image-upload'),
    path('uploaded_images/<int:pk>/', UploadedImagesRetrieveUpdateDestroyView.as_view(),
         name='image-retrieve-update-destroy'),
    path('subcription/', SubscriptionAPIView.as_view(), name='subcription'),

]

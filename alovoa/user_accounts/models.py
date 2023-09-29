from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_for =  models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    religion = models.CharField(max_length=255, null=True, blank=True)
    community = models.CharField(max_length=255, null=True, blank=True)
    living_in = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=155, null=True, blank=True)

    def __str__(self):
        return self.username



class Subscription(models.Model):
    SUBSCRIPTION_CHOICES = (
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

class UserLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes_given')
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes_received')
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    slug = models.CharField(max_length=1000, null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.user.username} likes {self.liked_user.username}'


class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

class UploadedImages(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default = "3")
    image  = models.ImageField(upload_to="uploaded_images",default='uploaded_default.jpg')

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    religion = models.CharField(max_length=255, null=True, blank=True)
    caste = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hobbies = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username

class Userdata(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_image = models.ForeignKey(UploadedImages, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class ProfilePicture(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
    image = models.ImageField(upload_to="profile_pictures", default="default.jpg")

    def __str__(self):
        return self.user.username

class Preference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    min_age = models.IntegerField(null=True, blank=True)
    max_age = models.IntegerField(null=True, blank=True)
    min_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    religion_preference = models.CharField(max_length=255, null=True, blank=True)
    caste_preference = models.CharField(max_length=255, null=True, blank=True)
    marital_status_preference = models.CharField(max_length=20, null=True, blank=True)
    education_preference = models.CharField(max_length=255, null=True, blank=True)
    occupation_preference = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Religion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Community(models.Model):
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name



class State(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    def __str__(self):
        return self.name









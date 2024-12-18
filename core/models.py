from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime



# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.CharField(max_length=500, blank=True)
    profileimg =models.ImageField( upload_to='profile_images', default='black-img.jpg')
    location = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username
    


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    user= models.CharField( max_length=100)
    image = models.ImageField( upload_to="post_image", )
    caption =models.TextField()
    created_at = models.DateTimeField(default= datetime.now)
    no_of_like = models.IntegerField(default=0)


    def __str__(self):
        return self.user
    

class Likepost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField( max_length=50)

    def __str__(self):
        return self.username


class FollowersCount(models.Model):
    follower = models.CharField( max_length=100)
    user = models.CharField( max_length=100)

    def __str__(self):
        return self.user
    

    

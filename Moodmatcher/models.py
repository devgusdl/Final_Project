# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.staticfiles import finders


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=20, default='community')  # 또는 'customer-service'로 설정
    likes = models.ManyToManyField(User, related_name='liked_posts')  # 여기서 related_name을 업데이트하세요
    new_likes = models.IntegerField(default=0)

    
    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')

    def __str__(self):
        return f"Image {self.pk}"


def default_profile_picture():
    default_image_path = finders.find('images/default_profile.png')

    if default_image_path:
        default_image_path = default_image_path.replace("\\", "/")  # Windows 경로에서 슬래시로 변경
    else:
        default_image_path = '/static/images/profile.png'

    return default_image_path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default=default_profile_picture)

    def __str__(self):
        return self.user.username


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'

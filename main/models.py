from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg', blank=True)
    website = models.URLField(blank=True)
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Profile of {self.user.username}'

class News(models.Model):
    title = models.CharField(max_length=200)
    precontent = models.TextField(blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.pk})

class Article(models.Model):
    title = models.CharField(max_length=200)
    precontent = models.TextField(blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images/', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
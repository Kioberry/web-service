from django.db import models
from django.contrib.auth.hashers import make_password
from django.conf import settings

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class NewsStory(models.Model):
    CATEGORY_CHOICES = (
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    )

    REGION_CHOICES = (
        ('uk', 'United Kingdom'),
        ('eu', 'Europe'),
        ('w', 'World'),
    )

    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline

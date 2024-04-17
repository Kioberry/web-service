from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)


    def save(self, *args, **kwargs):
        # 如果密码被更改，确保它是哈希过的
        if self._state.adding and not self.id:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """
        如果给定的原始密码正确，返回True，否则返回False。
        """
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)
    

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

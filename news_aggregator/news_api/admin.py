from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Author, NewsStory

admin.site.register(Author)
admin.site.register(NewsStory)

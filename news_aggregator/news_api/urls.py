from django.urls import path
from . import views
# Make sure to include these URLs in the main project's urls.py file
urlpatterns = [
    path('api/login/', views.login_view, name='login'),
    path('api/logout/', views.logout_view, name='logout'),
    path('api/stories/', views.post_story_view, name='post_story'),
    path('api/stories/get/', views.get_stories_view, name='get_stories'),
]



from django.urls import path
from . import views

urlpatterns = [
    path('api/login', views.login_view, name='login'),
    path('api/logout', views.logout_view, name='logout'),
    path('api/stories', views.stories_view, name='stories'),
    path('api/stories/<int:key>', views.delete_story_view, name='delete_story'),
]




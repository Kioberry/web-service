# from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import NewsStory, Author
import json
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_list_or_404, get_object_or_404
import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(['POST'])# ensure that this view can only be called by POST request
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Logged in successfully"}, status=200)
    else:
        return JsonResponse({"message": "Invalid credentials"}, status=400)


@require_http_methods(['POST']) # ensure that this view can only be called by POST request
def logout_view(request):
    try:
        # here we suggest user has logged in
        logout(request)
        return JsonResponse({"message": "Logged out successfully"}, status=200)
    except Exception as e:
        # If any error happen, return error message
        return JsonResponse({"error": str(e)}, status=500)



@require_http_methods(['POST'])
def post_story_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Please login to post a story"}, status=503, content_type='text/plain')

    try:
        data = json.loads(request.body)
        try:
            author = Author.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Author not found."}, status=503, content_type='text/plain')

        news_story = NewsStory.objects.create(
            headline=data['headline'],
            category=data['category'],
            region=data['region'],
            details=data['details'],
            author=author
        )
        return JsonResponse({"message": "Story posted successfully", "id": news_story.id}, status=201)

    except (IntegrityError, ValidationError, ValueError) as e:
        # Catch possible exceptions such as data integrity issues, validation errors, or JSON parsing errors
        return JsonResponse({"message": str(e)}, status=503, content_type='text/plain')



@require_http_methods(['GET'])
def get_stories_view(request):
    # get query parameters
    category = request.GET.get('story_cat', '*')
    region = request.GET.get('story_region', '*')
    date = request.GET.get('story_date', '*')
    
    query = {}
    if category != '*':
        query['category'] = category
    if region != '*':
        query['region'] = region
    if date != '*':
        try:
            query['date__gte'] = datetime.datetime.strptime(date, '%d/%m/%Y').date()
        except ValueError:
            return JsonResponse({"message": "Invalid date format"}, status=400)
    
    # get stories list, return 404 if not found
    try:
        stories = get_list_or_404(NewsStory.objects.filter(**query).values(
            'id', 'headline', 'category', 'region', 'author__name', 'date', 'details'))
        return JsonResponse({"stories": list(stories)}, status=200)
    except ValidationError:
        return JsonResponse({"message": "No stories found"}, status=404, content_type='text/plain')

@require_http_methods(['DELETE'])
@login_required
def delete_story_view(request, key):
    try:
        story = get_object_or_404(NewsStory, pk=key)
        story.delete()
        return JsonResponse({"message": "Story deleted successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=503, content_type='text/plain')
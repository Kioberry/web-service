# from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
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
@require_http_methods(['POST'])  # 确保该视图只能通过 POST 请求调用
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not request.user.is_authenticated:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Logged in successfully", content_type="text/plain", status=200)
        else:
            return HttpResponse("Invalid credentials", content_type="text/plain", status=401)  # 使用 401 状态码表示认证失败
    else:
        return HttpResponse("You have already logged in", content_type="text/plain", status=200)




@csrf_exempt
@require_http_methods(['POST']) # ensure that this view can only be called by POST request
def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("You have not logged in", content_type="text/plain", status=500)    
    try:
        # here we suggest user has logged in
        logout(request)
        return HttpResponse("Logged out successfully", content_type="text/plain", status=200)    
    except Exception as e:
        # If any error happen, return error message
        return HttpResponse(str(e), content_type="text/plain", status=500)  



@csrf_exempt
def post_story_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("Please login before posting stories", content_type="text/plain", status=503)

    try:
        data = json.loads(request.body)
        if 'headline' not in data or 'category' not in data or 'region' not in data or 'details' not in data:
            return HttpResponse("Missing required story fields", content_type="text/plain", status=503)
        
        # Validate category and region against predefined choices
        valid_categories = [choice[0] for choice in NewsStory.CATEGORY_CHOICES]
        valid_regions = [choice[0] for choice in NewsStory.REGION_CHOICES]
        if data['category'] not in valid_categories:
            return HttpResponse("Invalid category option", content_type="text/plain", status=400)
        if data['region'] not in valid_regions:
            return HttpResponse("Invalid region option", content_type="text/plain", status=400)

        try:
            author = Author.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return HttpResponse("Author not found", content_type="text/plain", status=503)

        news_story = NewsStory.objects.create(
            headline=data['headline'],
            category=data['category'],
            region=data['region'],
            details=data['details'],
            author=author,
            date=datetime.datetime.now()  # Assuming your model has a date field to capture the timestamp
        )
        return HttpResponse(f"Story posted successfully, ID: {news_story.id}", content_type="text/plain", status=201)

    except (IntegrityError, ValidationError, ValueError) as e:
        return HttpResponse(f"Error posting story: {str(e)}", content_type="text/plain", status=503)



def get_stories_view(request):
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
            return HttpResponse("Invalid date format", content_type="text/plain", status=404)

    stories = NewsStory.objects.filter(**query).values(
        'id', 'headline', 'category', 'region', 'author__name', 'date', 'details')

    if not stories:
        return HttpResponse("No stories found", content_type="text/plain", status=404)

    # Formatting the list of stories as a plain text string
    stories_text = "\n".join(f"ID: {story['id']}, Headline: {story['headline']}, Category: {story['category']}, "
                             f"Region: {story['region']}, Author: {story['author__name']}, Date: {story['date'].strftime('%Y-%m-%d')}, "
                             f"Details: {story['details']}"
                             for story in stories)
    return HttpResponse(stories_text, content_type="text/plain", status=200)



@csrf_exempt
def stories_view(request):
    if request.method == 'POST':
        return post_story_view(request)
    elif request.method == 'GET':
        return get_stories_view(request)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
@login_required
@require_http_methods(['DELETE'])
def delete_story_view(request, key):
    try:
        story = get_object_or_404(NewsStory, pk=key)
        story.delete()
        return HttpResponse("Story deleted successfully", content_type="text/plain", status=200)

    except Exception as e:
        return HttpResponse(str(e), content_type="text/plain", status=503)

    

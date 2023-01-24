from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    news = Post.objects.all().order_by("dateCreation").reverse()
    # news = Post.objects.all().order_by("-id")
    return render(request, 'index.html', context={'news': news})

def detail(request, id):
    new = Post.objects.get(id=id)
    post_comments = Comment.objects.filter(commentPost=Post.objects.get(id=id))
    post_comments_count = Comment.objects.filter(commentPost=Post.objects.get(id=id)).count()
    #post_comments_values = post_comments.values('dateCreation', 'commentUser', 'rating', 'text')
    #print(post_comments_values)
    return render(request, 'details.html', context={'new': new, 'post_comments': post_comments, 'post_comments_count': post_comments_count})


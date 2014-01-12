from django.shortcuts import render
from django.http import HttpResponse

from blog.models import Post

def index(request):
  posts = Post.objects.filter(published=True)
  return render(request, 'blog/index.html', {'posts': posts})

def post(request, id):
  post = Post.objects.get(id = id)
  return render(request, 'blog/post.html', { 'post': post} )

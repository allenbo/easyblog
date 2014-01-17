from django.shortcuts import render
from django.http import HttpResponse

from blog.models import Post, Reply

def index(request):
  posts = Post.objects.filter(published=True)
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  return render(request, 'blog/index.html', {'posts': posts, 'recent_post':recent_post,
    'recent_reply':recent_reply})

def post(request, id):
  post = Post.objects.get(id = id)
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  return render(request, 'blog/post.html', { 'post': post, 'recent_post':recent_post,
    'recent_reply':recent_reply} )


def about(request):
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  return render(request, 'about.html', {'recent_post': recent_post, 'recent_reply':recent_reply } )

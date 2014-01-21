from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from blog.forms import ReplyForm

from blog.models import Post, Reply, Category

def index(request):
  posts = Post.objects.filter(published=True)
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  categories = Category.objects.all()
  archives = None
  if posts:
    archives = posts[0].get_archive()
    print archives
  return render(request, 'blog/index.html', {'posts': posts, 'recent_post':recent_post,
    'recent_reply':recent_reply, 'categories': categories, 'archives':archives})

def post(request, id):
  post = Post.objects.get(id = id)
  post.visit += 1
  post.save()
  replies = Reply.objects.filter(post = post)
  categories = Category.objects.all()
  form = ReplyForm(initial = {'blog_id':id})
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  archives = None
  archives = post.get_archive()
  return render(request, 'blog/post.html', { 'post': post, 'recent_post':recent_post,
    'recent_reply':recent_reply, 'form': form, 'replies': replies, 'categories': categories,
    'archives':archives} )

def message(request):
  errors = []
  if request.method == 'POST':
    form = ReplyForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      Reply.insert_from_form(cd)
      return HttpResponseRedirect('/blog/%s/' % cd['blog_id'])
    else:
      pass
  else:
    return render(request, 'message_error.html', {'errors': errors})

def category(request, name):
  cate = Category.objects.get(name = name)
  posts = Post.objects.filter(published=True, category = cate)
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  categories = Category.objects.all()
  archives = None
  if posts:
    archives = posts[0].get_archive()
    print archives
  return render(request, 'blog/index.html', {'posts': posts, 'recent_post':recent_post,
    'recent_reply':recent_reply, 'categories': categories, 'archives':archives})


def about(request):
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  return render(request, 'about.html', {'recent_post': recent_post, 'recent_reply':recent_reply } )

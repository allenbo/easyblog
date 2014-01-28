from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from blog.forms import ReplyForm

from blog.models import Post, Reply, Category
from django.db.models import Q  

def index(request):
  posts = Post.objects.filter(published=True)
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  categories = Category.objects.all()
  archives = None
  archives = Post.get_archive()
  return render(request, 'blog/index.html', {'posts': posts, 'recent_post':recent_post,
    'recent_reply':recent_reply, 'categories': categories, 'archives':archives})

def post(request, mangled):
  preview = None
  if mangled:
    title = mangled.replace('__', ' ')
    post = Post.objects.get(title = title)
    post.visit += 1
    post.save()
  else:
    errors = []
    if request.method == 'GET' and request.GET.get('id', ''):
      id = request.GET['id']
      post = Post.objects.get(id = id)
      
      if not post or post.published == True:
        return render(request, 'admin/error.html', {'errors':errors})
      preview = True
    else:
      return render(request, 'admin/error.html', {'errors':errors})
  replies = Reply.objects.filter(post = post)
  categories = Category.objects.all()
  form = ReplyForm(initial = {'blog_id':post.id})
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  archives = Post.get_archive()
  return render(request, 'blog/post.html', {'preview':preview, 'post': post, 'recent_post':recent_post,
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
  archives = Post.get_archive()
  return render(request, 'blog/index.html', {'posts': posts, 'recent_post':recent_post,
    'recent_reply':recent_reply, 'categories': categories, 'archives':archives})


def search(request):
  errors = []
  if request.method == 'GET':
    try:
      q = request.GET['q']
      posts = Post.objects.filter(published = True, content__contains = q)
      recent_post = Post.objects.first()
      recent_reply = Reply.objects.first()
      categories = Category.objects.all()
      archives = None
      archives = Post.get_archive()
      return render(request, 'blog/index.html', {'posts': posts, 'recent_post':recent_post,
        'recent_reply':recent_reply, 'categories': categories, 'archives':archives})
    except KeyError:
      return HttpResponse('Errors')

  



def archive(request, year, month = None):
  if month is None:
    posts = Post.objects.filter(published=True, created_date__year = year)
  else:
    posts = Post.objects.filter(published=True, created_date__year = year, created_date__month = month)
  cate = Category.objects.all()
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  categories = Category.objects.all()
  archives = None
  if posts:
    archives = posts[0].get_archive()
  return render(request, 'blog/index.html', {'posts': posts, 'recent_post':recent_post,
    'recent_reply':recent_reply, 'categories': categories, 'archives':archives})

  

def about(request):
  recent_post = Post.objects.first()
  recent_reply = Reply.objects.first()
  return render(request, 'about.html', {'recent_post': recent_post, 'recent_reply':recent_reply } )

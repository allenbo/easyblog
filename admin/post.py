from blog.models import Post, Reply, Category
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def get_posts_from_action(request):
  post_state = 'all'
  if 'published' in request.GET and request.GET['published'] == 'yes':
    posts = Post.objects.filter(published = True)
    post_state = 'published'
  elif 'draft' in request.GET and request.GET['draft'] == 'yes':
    posts = Post.objects.filter(published = False)
    post_state = 'draft'
  else:
    posts = Post.objects.all()

  return post_state, posts


def get_posts_from_state(post_state, **kw):
  if post_state == 'published':
    return Post.objects.filter(published = True , **kw)
  elif post_state == 'draft':
    return Post.objects.filter(published = False, **kw)
  else:
    return Post.objects.filter(**kw)

@login_required
def show(request):
  allpost = Post.objects.count()
  published = Post.objects.filter(published = True).count()
  draft = allpost - published

  context = {'num_allpost':allpost, 'num_published':published, 'num_draft':draft}
  if request.method == 'GET':
    if 'action' in request.GET:
      post_state, posts = get_posts_from_action(request)
      context['post_state'] = post_state
      context['posts'] = posts
      return render(request, 'admin/post_show.html', context)
    else:
      if 'q' in request.GET and request.GET['q']:
        post_state = request.GET.get('post_state', 'all')
        q = request.GET['q']
        kw = {}
        kw['content__icontains'] = q
        posts = get_posts_from_state(post_state, **kw)

        context['post_state'] = post_state
        context['posts'] = posts
        return render(request, 'admin/post_show.html', context)

  elif request.method == 'POST':
    errors = []
    next = request.get_full_url()
    return render (request, 'admin/error.html', {'errors': errors, 'next':next })
  posts = Post.objects.all()
  context['post_state'] = 'all'
  context['posts'] = posts
  return render(request, 'admin/post_show.html', context)

  
@login_required
def edit(request):
  context = {}
  context['categories'] = Category.objects.all()
  errors = []
  if request.method == 'GET':
    if 'action' in request.GET:
      action = request.GET['action']
      if action == 'add':
        return render(request, 'admin/post_edit.html', context)
      elif action == 'edit':
        if 'id' in request.GET and request.GET['id']:
          post = Post.objects.get(id = request.GET['id'])
          if not post:
            return render(request, 'admin/erorr.html', {'errors':errors})
          context['post'] = post
          return render(request, 'admin/post_edit.html', context)
  else:
    return render(request, 'admin/error.html', {'errors':errors})


def check_edit_post_param(dic):
  if not dic.get('post_title', ''):
    return False

  if not dic.get('content', ''):
    return False

  if not dic.get('category', ''):
    return False

  if dic.get('published', '') not in ('Save Draft', 'Publish'):
    return False

  return True

@login_required
def add(request):
  if request.method == 'POST':
    if check_edit_post_param(request.POST):
      author = request.user
      id = Post.insert_from_dic(request.POST, author = request.user)
      link = '/admin/post'
      if request.POST['published'] == 'Save Draft':
        link = '/admin/post/edit/?action=edit&id=%d' % id
      return HttpResponseRedirect(link)
  errors = []
  return render(request, 'admin/error.html', {'errors':errors})

@login_required
def modify(request):
  errors = []
  if request.method == 'POST':
    dic = request.POST
    if check_edit_post_param(request.POST):
      post_id = dic.get('id', '')
      post = Post.objects.get(id = post_id)

      if post:
        post.modify_from_dic(request.POST)
        link = '/admin/post/'
        if request.POST['published'] == 'Save Draft':
          link = '/admin/post/edit/?action=edit&id=%d' % post.id
        return HttpResponseRedirect(link)
  return render(request, 'admin/error.html', {'errors':errors})



@login_required
def delete(request):
  errors = []
  if request.method == 'GET':
    dic = request.GET
    if dic.get('action', '') == 'delete' and dic.get('id', ''):
      id = dic['id']
      post = Post.objects.get(id = id)

      if post:
        post.delete()
        return HttpResponseRedirect('/admin/post/')
  
  return render(request, 'admin/error.html', {'errors':errors})

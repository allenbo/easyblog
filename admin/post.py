from blog.models import Post, Reply, Category
from django.shortcuts import render

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

  
def new(request):
  pass

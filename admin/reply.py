from blog.models import Post, Reply, Category
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def get_reply_from_filter(request):
  state = 'pending'
  if 'state' in request.GET and request.GET['state']:
    state = request.GET['state']
  replies = Reply.objects.filter(state = Reply.state_choice(state))
  return state, replies
  

def get_replies_from_state(state, **kw):
  if state == 'all':
    return Reply.objects.filter(**kw)
  state = Reply.state_choice(state)
  kw.update({'state':state})
  return Reply.objects.filter(**kw)

@login_required
def show(request): 
  context = Reply.get_num_of_state()
  if request.method == 'GET':
    if 'filter' in request.GET and request.GET['filter'] == 'true':
      state, replies = get_reply_from_filter(request)
      context['state'] = state
      context['replies'] = replies
      return render(request, 'admin/reply_show.html', context)
    else:
      kw = {}
      errors = []
      state = request.GET.get('state', 'all')
      if 'action' in request.GET and request.GET['action'] == 'search':
        name = request.GET.get('name', '')
        email = request.GET.get('email', '')
        if name and email:
          kw = {'name':name, 'email':email}
        else:
          return render(request, 'admin/error.html', {'errors':errors})
      elif 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        kw = {'q':q}
      replies = get_replies_from_state(state, **kw)
      context['state'] = state
      context['replies'] = replies
      return render(request, 'admin/reply_show.html', context)
  elif request.method == 'POST':
    errors = []
    return render(request, 'admin/error.html', {'errors': errors})


@login_required
def edit(request):
  errors = []
  if request.method == 'GET':
    id = request.GET.get('id', '')
    action = request.GET.get('action', '')
    if id and action:
      reply = Reply.objects.get(id = id)
      if reply:
        reply.action(action)
        state = 'pending' if action in ('delete', 'restore') else action
        return HttpResponseRedirect('/admin/reply/show/?filter=true&state=%s' % state)
    return render(request, 'admin/error.html', {'errors':errors})
  else:
    return render(request, 'admin/error.html', {'errors':errors})

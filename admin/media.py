from blog.models import Post, Reply, Category, Media
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from admin.forms import MediaForm
from admin.forms import MediaFilterForm

@login_required
def show(request):
  context = Media.get_num_of_state()
  if request.method == 'GET' and request.GET:
    form = MediaFilterForm(request.GET)
    if form.is_valid():
      attached = form.cleaned_data['attached']
      if attached == 'true':
        medias = Media.objects.filter(attached = True)
      else:
        medias = Media.objects.filter(attached = False)
    else:
      return render(request, 'admin/error.html')
  else:
    medias = Media.objects.all()
  context['medias'] = medias
  return render(request, 'admin/media_show.html', context)


@login_required
def search(request):
  context = Media.get_num_of_state()
  if request.method == 'GET' and 'q' in request.GET:
    q = request.GET.get('q', '')
    if q:
      medias = Media.objects.filter(description__icontains = q)
      context['medias'] = medias
      return render(request, 'admin/media_show.html', context)
  else:
    return render(request, 'admin/error.html')



@login_required
def upload(request):
  if request.method == 'POST':
    form = MediaForm(request.POST, request.FILES)
    if form.is_valid():
      print form.cleaned_data
      new = form.save()
      new.generate_icon()
      return HttpResponseRedirect('/admin/media/')
  else:
    return render(request, 'admin/media_edit.html')
  

@login_required
def delete(request):
  if request.method == 'GET':
    if 'action' in request.GET and request.GET['action']:
      if request.GET['action'] == 'delete':
        media = Media.objects.get(id = request.GET['id'])
        if media:
          media.delete()
          return HttpResponseRedirect("/admin/media/show/")
  return render(request, 'admin/error.html')
  


@login_required
def edit(request):
  if request.method == 'GET':
    media = Media.objects.get(id = request.GET.get('id', ''))
    if media:
      if request.GET.get('action', '') == 'edit':
        return render(request, 'admin/media_edit.html', {'media':media})
      else:
        form = MediaForm(request.GET, instance = media)
        if form.is_valid():
          form.save()
          return HttpResponseRedirect("/admin/media/show/")
  return render(request,'admin/error.html')

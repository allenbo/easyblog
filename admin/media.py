from blog.models import Post, Reply, Category, Media
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from admin.forms import MediaForm



@login_required
def show(request):
  context = Media.get_num_of_state()
  medias = Media.objects.all()
  context['medias'] = medias
  return render(request, 'admin/media_show.html', context)



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
    form = MediaForm()
    return render(request, 'admin/media_upload.html', {'form':form})
  


@login_required
def edit(request):
  pass


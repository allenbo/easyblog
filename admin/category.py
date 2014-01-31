from blog.models import Post, Reply, Category
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def show(request):
  categories = Category.objects.all()
  context = {}
  context['categories'] = categories
  return render(request, 'admin/category_show.html', context)

from blog.models import Post, Reply, Category
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def show(request):
  categories = Category.objects.all()
  if request.method == 'GET':
    if 'q' in request.GET and not request.GET['q']:
      q = request.GET['q']
      kw = {}
      categories = Category.objects.filter(desciption__icontains  =  q)
  context = {}
  context['categories'] = categories
  return render(request, 'admin/category_show.html', context)


@login_required
def edit(request):
  categories = Category.objects.all()
  context = {}
  context['categories'] = categories
  
  errors = []
  if request.method == 'GET':
    if 'action' in request.GET:
      action = request.GET.get('action', 'add')
      if action == 'add':
        return render(request, 'admin/category_edit.html', context)
      elif action == 'edit':
        if 'id' in request.GET and request.GET['id']:
          category = Category.objects.get(id = request.GET['id'])
          if category:
            context['category'] = category
            return render(request, 'admin/category_edit.html', context)
    return render(request, 'admin/error.html', {'errors':errors}) 


def check_edit_post_param(dic):
  if not dic.get('name',''):
    return False
  
  if not dic.get('parent', ''):
    return False

  parent = dic.get('parent')
  if parent == '-1':
    return True
  else:
    try:
      parent = int(parent)
    except ValueError:
      return False
    else:
      return Category.objects.filter(id = parent) is not None

  return True

@login_required
def add(request):
  errors = []
  if request.method == 'POST':
    print request.POST
    if check_edit_post_param(request.POST):
      Category.insert_from_dic(request.POST.copy())
      return HttpResponseRedirect('/admin/category/show/')
  return render(request, 'admin/error.html', {'errors':errors})


@login_required
def modify(request):
  errors = []
  if request.method == 'POST':
    dic = request.POST
    if check_edit_post_param(dic):
      category_id = request.POST.get('id', '')
      category = Category.objects.get(id = category_id)

      if category:
        category.modify_from_dic(dic)
        return HttpResponseRedirect('/admin/category/show/')
  return render(request, 'admin/error.html', {'errors':errors})


@login_required
def delete(request):
  errors = []
  if request.method == 'GET':
    dic = request.GET
    if dic.get('action', '') == 'delete' and dic.get('id', ''):
      id = dic['id']
      category = Category.objects.get(id = id)
      if category:
        category.delete()
        Category.objects.filter(has_parent = 1, parent_id = id).update(has_parent=0)
        return HttpResponseRedirect('/admin/category/show')

  return render(request, 'admin/error.html', {'errors':errors})

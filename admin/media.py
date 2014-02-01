from blog.models import Post, Reply, Category
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required



@login_required
def show(request):
  pass



@login_required
def upload(request):
  pass


@login_required
def delete(request):
  pass

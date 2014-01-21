from django.db import models
from datetime import datetime

# Create your models here.


class Category(models.Model):
  name = models.CharField(max_length=100)

  def get_num(self):
    return Category.objects.filter(name = self.name).count()


class Post(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(max_length = 100)
  content = models.TextField()
  published = models.BooleanField(default = False)
  created_date = models.DateTimeField(auto_now_add = True)
  category = models.ManyToManyField(Category)
  visit = models.IntegerField()


  class Meta:
    ordering = ['-created_date']

  def __unicode__(self):
    return self.title

  def get_abs_url(self):
    return '/blog/%s' % self.id

  def get_visit_num(self):
    return self.visit

  def get_reply_num(self):
    return Reply.objects.filter(post = self).count()


  def get_prev_post(self):
    if self.id == 1:
      return None
    else:
      return Post.objects.get(id = self.id - 1)

  def get_next_post(self):
    if self.id == Post.objects.count():
      return None
    else:
      return Post.objects.get(id = self.id + 1)

  @staticmethod
  def get_archive():
    return Post.objects.values('created_date').distinct()



class Reply(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(blank = True)
  to = models.IntegerField(default=0)
  message = models.CharField(max_length = 1000)
  post = models.ForeignKey(Post)
  date = models.DateTimeField()


  @staticmethod
  def insert_from_form(cd):
    post = Post.objects.get(id = int(cd['blog_id']))
    date = datetime.now()
    Reply(name = cd['name'], email = cd['email'], to = '0', message = cd['message'], post = post,
        date=date).save()

  

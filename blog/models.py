from django.db import models

# Create your models here.


class Category(models.Model):
  name = models.CharField(max_length=100)


class Post(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(max_length = 100)
  content = models.TextField()
  published = models.BooleanField(default = False)
  created_date = models.DateTimeField(auto_now_add = True)
  category = models.ManyToManyField(Category)


  class Meta:
    ordering = ['-created_date']

  def __unicode__(self):
    return self.title

  def get_abs_url(self):
    return 'blog/%s' % self.id

  def get_visit_num(self):
    return 0

  def get_reply_num(self):
    return 0


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



class Reply(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(blank = True)
  to = models.IntegerField(default=0)
  message = models.CharField(max_length = 1000)
  post = models.ForeignKey(Post)


  @staticmethod
  def insert_from_form(cd):
    post = Post.objects.get(id = int(cd['blog_id']))
    Reply(name = cd['name'], email = cd['email'], to = '0', message = cd['message'], post = post).save()

  

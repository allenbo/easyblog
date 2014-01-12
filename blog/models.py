from django.db import models

# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(max_length = 100)
  content = models.TextField()
  published = models.BooleanField(default = False)
  created_date = models.DateTimeField(auto_now_add = True)



  class Meta:
    ordering = ['-created_date']

  def __unicode__(self):
    return self.title

  def get_abs_url(self):
    return 'blog/%s' % self.id

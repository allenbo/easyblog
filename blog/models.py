from django.db import models
from datetime import datetime
from easyblog.settings import ROOT_DIR, MEDIA_URL
import os
import Image
import common

# Create your models here.


class Category(models.Model):
  name = models.CharField(max_length=100)
  has_parent = models.BooleanField()
  parent_id = models.IntegerField(blank=True)
  description = models.CharField(max_length = 1000)


  def get_parent(self):
    if not self.has_parent:
      return None
    else:
      return Category.objects.get(id = self.parent_id)

  @property
  def post(self):
    return Post.objects.filter(category = self)
    
  @staticmethod
  def insert_from_dic(dic):
    parent = int(dic['parent'])
    if parent == -1:
      has_parent = 0
    else:
      has_parent = 1
    name = dic['name']
    description = dic['description']

    Category(name = name, has_parent = has_parent, parent_id = parent, description = description ).save()


  def modify_from_dic(self, dic):
    parent = int(dic['parent'])
    if parent == -1:
      self.has_parent = 0
    else:
      self.has_parent = 1
      self.parent_id = parent
    self.name = dic['name']
    self.description = dic['description']
    self.save()
    


class Tag(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length = 1000)


class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  author = models.CharField(max_length=100)
  published = models.BooleanField(default = False)
  created_date = models.DateTimeField(auto_now_add = True)
  category = models.ForeignKey(Category, default = 1, on_delete = models.SET_DEFAULT)
  tags = models.ManyToManyField(Tag)
  visit = models.IntegerField()


  class Meta:
    ordering = ['-created_date']


  def __unicode__(self):
    return self.title

  def get_abs_url(self):
    mangled = self.title.replace(' ', '__')
    return '/blog/%s/' % mangled

  def get_visit_num(self):
    return self.visit

  def get_reply_num(self):
    return Reply.objects.filter(post = self, state = Reply.APPROVED).count()


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
    dates = Post.objects.values('created_date').distinct()
    blog_dates = []
    for date in dates:
      archive_date = datetime(year = date['created_date'].year, month = date['created_date'].month,
          day = 1)
      if archive_date not in blog_dates:
        blog_dates.append(archive_date)
    return blog_dates

  @staticmethod
  def insert_from_dic(dic, author = None):
    published = True if dic.get('published', 'Publish') == 'Publish' else False
    cate = Category.objects.get(name = dic['category'])
    if not cate:
      cate = Category.objects.get(name == 'Uncategoried')

    if author is None:
      author = 'abo'
    post = {'title':dic['post_title'], 'author': author, 'published':published, 'category': cate,
        'content':dic['content']}
    post['created_date'] = dic.get('created_date', datetime.now())
    post['visit'] = 0
    p = Post(**post)
    p.save()
    
    return p.id


  def modify_from_dic(self, dic):
    published = True if dic.get('published', 'Publish') == 'Publish' else False
    cate = Category.objects.get(name = dic['category'])
    if not cate:
      cate = Category.objects.get(name == 'Uncategoried')

    self.title = dic['post_title']
    self.content = dic['content']
    self.author = 'admin'
    self.published = published
    self.category = cate
    self.save()



class Reply(models.Model):
  APPROVED = 'ap'
  PENDING = 'pd'
  SPAM = 'sp'
  TRASH = 'tr'
  STATE_CHOICE = (
      (TRASH, 'trash'),
      (APPROVED, 'approved'),
      (PENDING, 'pending'),
      (SPAM, 'spam'),
  )
  name = models.CharField(max_length=100)
  email = models.EmailField()
  to = models.IntegerField(default=0)
  message = models.CharField(max_length = 1000)
  post = models.ForeignKey(Post)
  date = models.DateTimeField()
  state = models.CharField(max_length = 2, choices = STATE_CHOICE, default = PENDING)

  @staticmethod
  def state_choice(state):
    for choice in Reply.STATE_CHOICE:
      if choice[1] == state:
        return choice[0]
    return 'pd'

  @staticmethod
  def insert_from_form(cd):
    post = Post.objects.get(id = cd['blog_id'])
    date = datetime.now()
    reply = Reply(name = cd['name'], email = cd['email'], to = '0', message = cd['message'], post = post,
        date=date, state = Reply.PENDING)
    reply.save()

    return post,reply 


  @staticmethod
  def get_num_of_state():
    all = Reply.objects.count()
    pending = Reply.objects.filter(state = Reply.PENDING).count()
    approved = Reply.objects.filter(state = Reply.APPROVED).count()
    spam = Reply.objects.filter(state = Reply.SPAM).count()
    trash = all - pending - approved - spam

    dic = {'num_allreply': all,
               'num_pending':pending,
               'num_approved':approved,
               'num_spam':spam,
               'num_trash':trash
               }
    return  dic

  def action(self, action):
    if action == 'delete':
      self.delete()
      return
    self.state = Reply.state_choice(action)
    self.save()

def to_icon(url):
  icon_url = '_icon.'.join(url.rsplit('.', 1))
  return icon_url


class Media(models.Model):
  name = models.CharField(max_length = 100)
  caption = models.CharField(max_length = 100, blank = True)
  alternative = models.CharField(max_length = 100, blank = True)
  description =  models.TextField(max_length = 1000, blank = True)
  attached = models.BooleanField(default = False)
  post = models.ForeignKey(Post, null = True, blank = True, default = None, on_delete = models.SET_NULL)
  date = models.DateTimeField(default = datetime.now)
  file = models.ImageField(upload_to="images/%Y/%m/%d/")


  class Meta:
    ordering = ['-date']


  
  def generate_icon(self):
    origin_path = os.path.join(ROOT_DIR, MEDIA_URL[1:], self.file.name)
    icon_path = os.path.join(ROOT_DIR, MEDIA_URL[1:], to_icon(self.file.name))
    common.resize_image(origin_path, 64, 64, icon_path)
    return True
   

  def get_icon_url(self):
    return to_icon(self.file.url)


  @staticmethod
  def get_num_of_state():
    all = Media.objects.count()
    attached = Media.objects.filter(attached = True).count()
    unattached = all - attached

    return {'num_allimage':all,
        'num_attached':attached,
        'num_unattached':unattached
        }

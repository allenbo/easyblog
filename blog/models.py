from django.db import models
from datetime import datetime

# Create your models here.


class Category(models.Model):
  name = models.CharField(max_length=100)
  has_parent = models.BooleanField()
  parent_id = models.IntegerField(blank=True)
  description = models.CharField(max_length = 1000)

  def get_num(self):
    return Category.objects.filter(name = self.name).count()


class Tag(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length = 1000)


class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  author = models.CharField(max_length=100)
  published = models.BooleanField(default = False)
  created_date = models.DateTimeField(auto_now_add = True)
  category = models.ForeignKey(Category)
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
      (TRASH, 'unapproved'),
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

from django.contrib import admin

# Register your models here.

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
  list_display = ['title']
  list_filter = ['published', 'created_date']
  search_fields = ['title', 'content']
  date_hierarchy = 'created_date'
  save_on_top = True
  preppopulated_fields = {'slug' : ('title', ) }


admin.site.register(Post, PostAdmin)

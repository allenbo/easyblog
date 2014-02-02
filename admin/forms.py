from  django import forms
from blog.models import Media

class MediaForm(forms.ModelForm):
  class Meta:
    model = Media
    fields = ['name', 'caption', 'file', 'alternative', 'description' ]

from  django import forms
from blog.models import Media

class MediaForm(forms.ModelForm):
  class Meta:
    model = Media
    fields = ['name', 'caption', 'file', 'alternative', 'description' ]


class VirtualForm(forms.Form):
  pass


class MediaFilterForm(VirtualForm):
  filter = forms.BooleanField()
  attached = forms.CharField()

  def clean_filter(self):
    filter = self.cleaned_data['filter']
    if not filter:
      raise forms.ValidationError('filter has to be true')
    return True

  def clean_attached(self):
    attached = self.cleaned_data['attached']
    if attached in ('true', 'false'):
      return attached
    raise forms.ValidationError('attached has to be false or true')

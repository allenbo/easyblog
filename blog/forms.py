from django import forms

class ReplyForm(forms.Form):
  email = forms.EmailField(required = False, widget = forms.TextInput(attrs= {"class":"text"}))
  name = forms.CharField(required = False, widget= forms.TextInput(attrs = {'class':'text'}))
  message = forms.CharField(widget=forms.Textarea(attrs = {'class':'text','cols':'60'}))
  blog_id = forms.CharField(widget=forms.HiddenInput)

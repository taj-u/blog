from django import forms
from .models import Comment
from django.http import request
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length = 31, label='Your name')
    email = forms.EmailField(label='Your email', widget=forms.TextInput(attrs={'placeholder': "john.doe@email.com"}))
    to = forms.EmailField(label='Share with', widget=forms.TextInput(attrs={'placeholder': "Email to"}))
    comments = forms.CharField(widget = forms.Textarea, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length = 25, label='Your name', initial='Taj uddin')
    email = forms.EmailField(initial='To')
    to = forms.EmailField(label='To')
    comments = forms.CharField(widget = forms.Textarea, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
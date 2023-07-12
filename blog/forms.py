from django import forms
from .models import Comment, Post
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


class ContactForm(forms.Form):
    name = forms.CharField(max_length = 31, label='Your name')
    email = forms.EmailField(label='Your email', widget=forms.TextInput(attrs={'placeholder': "john.doe@email.com"}))
    message = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'placeholder': 'Write your message here in less than 250 words'}), label='Your message')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if title:
            cleaned_data['slug'] = title

        return cleaned_data
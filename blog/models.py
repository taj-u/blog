from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
from django.contrib import admin
from django.urls import reverse


from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                     .filter(status='published')
                     
class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail',
        args=[self.publish.year,
        self.publish.month,
        self.publish.day, self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User,
                            null=True,
                            blank=True,
                            default=None,
                            on_delete=models.CASCADE,
                            related_name='comments')
    post = models.ForeignKey(Post,
                            on_delete = models.CASCADE,
                            related_name = 'comments')
    body = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add = True)
    edited = models.DateTimeField(auto_now = True) 
    active = models.BooleanField(default = True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'comment --> {self.body} \non the post --> {self.post}'
    
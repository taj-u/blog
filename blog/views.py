from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, ContactForm
from django.conf.global_settings import EMAIL_HOST_USER

from taggit.models import Tag
from rest_framework import viewsets

from .serializers import PostSerializer, CommentSerializer

def index(request):
    return render(request, 'base.html')


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag,])
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = { 'page': page,
                'posts': posts,
                'tag': tag
                }
    return render(request, 'blog/post/list.html', 
                  context)


@login_required
def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = get_object_or_404(User, id=request.user.id)
            new_comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':comment_form}
    return render(request, 'blog/post/detail.html', context)

@login_required
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read "\
                      f"'{post.title}'"
            sharer_comment = cd['comments']
            message = f"Hello there. We hope this email finds you well. You might find this interesting and informative too as {cd['name']} finds.\n"\
                        f"The link and Title of the post are below.\n\nThank you.\nBrainWaveBlog Team.\n\n"\
                        f"Title: {post.title}\nLink: {post_url}\n\n"\
                        f"And here's the comment of {cd['name']}({cd['email']}): '{sharer_comment}'\n"
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})
 

def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    sent = False
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
           cd = form.cleaned_data
           contact_user_name = cd['name']
           contact_user_email = cd['email']
           contact_user_message = cd['message']
           subject = f"BrainBlogWave: {contact_user_name}({contact_user_email}) wants to reach you out."
           send_mail(subject=subject, message=contact_user_message, from_email=EMAIL_HOST_USER,recipient_list=['tajcsebsmrstu@gmail.com'], fail_silently=False)
           sent = True
    else:
        form = ContactForm()
    context = {'form':form,
               'sent':sent}
    return render(request, 'blog/contact.html', context=context)


@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id = user_id)
    posts = user.posts.all()
    print(posts)
    comments = user.comments.all()
    print(comments)
    context = {
        'user':user,
        'posts': posts,
        'comments': comments
    }
    return render(request, 'blog/user_profile.html', context)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.published.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.conf.global_settings import EMAIL_HOST_USER

from taggit.models import Tag
# Create your views here.
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

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"cd['name'] recommends you read "\
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                      f"{cd['name']}'s comments '{cd['comments']}'"
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    if request.method == 'POST':
       return HttpResponse("Thank you. We'll reach you soon.")
    return render(request, 'blog/contact.html')


def profile(request, user_id):
    pass
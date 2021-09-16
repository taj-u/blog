from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

from taggit.models import Tag
# Create your views here.
def index(request):
    return render(request, 'blog/base.html', )

def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'page': page,
               'posts': posts,
               'tag': tag,
               }
    return render(request, 'blog/post/list.html', 
                  context)
                  
def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)
    comments = post.comments.filter(active=True)

    # Handling Comment Form
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog:post_list')
    else:
        comment_form = CommentForm()

    # Adding pagination in comments
    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]
    context = {
        'post': post,
        'page': page,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':comment_form,
        'similar_posts': similar_posts}
    return render(request, 'blog/post/detail.html', context)

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read "\
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                      f"{cd['name']}'s comments '{cd['comments']}'"
            send_mail(subject, message, 'admin@admin.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    context = {'post':post,
               'form':form, 
               'sent':sent}
    return render(request, 'blog/post/share.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {'error':'Invalid username or password'}
            return render(request, 'accounts/login.html', context)
        login(request, user)
        return redirect('/')
    return render(request, 'aoounts/login.html', context={})
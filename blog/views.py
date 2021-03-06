from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

# Create your views here.
def index(request):
    return render(request, 'base.html')

def post_list(request):
    posts = Post.objects.all().filter(status='published')    
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'page': page,
               'posts': posts}
    return render(request, 'blog/post/list.html', 
                  context)
            
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
            return redirect('blog:post_list')
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
                      f"{cd['name']}'s comments {cd['comments']}"
            send_mail(subject, message, 'admin@admin.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})


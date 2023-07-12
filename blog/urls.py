from django.urls import path
from . import views

app_name='blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('post/create', views.post_create, name='post_create'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/update', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete', views.post_delete, name='post_delete'),
    path('<int:post_id>/share', views.post_share, name='post_share'),
    path('about/', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('profile/<int:user_id>', views.profile, name='user_profile'),
    path('comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    
]
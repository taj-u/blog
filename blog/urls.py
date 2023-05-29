from django.urls import path
from . import views

app_name='blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share', views.post_share, name='post_share'),
    path('about/', views.about, name='about'),
    path('contact', views.contact, name='contact'),


]
from django.urls import path
from django.urls.conf import include
from django.urls.resolvers import URLPattern
from . import views

app_name='blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.post_list, name='post_list'),
    path('login/', views.login_view, name='login_view'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>', views.post_list, name='post_list_by_tag'),
    path('<int:post_id>/share', views.post_share, name='post_share')
]
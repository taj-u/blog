from django.urls import path
from django.urls.conf import include
from django.urls.resolvers import URLPattern
from . import views

app_name='blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('all/', views.post_list, name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share', views.post_share, name='post_share')
]
from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    path('', views.index, name='index'),
    path('blog_details/<str:blog_id>/', views.blog_details, name='blog-details'),
    path('new_blog/', views.new_blog, name='new-blog'),
    path('edit_blog/<str:blog_id>/', views.edit_blog, name='edit-blog'),
    path('new_comment/<str:blog_id>/', views.new_comment, name='new-comment'),
]
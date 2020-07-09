from django.urls import path
from . import views

app_name = 'journals' #adding namespace for template to reference to
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<str:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<str:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<str:entry_id>', views.edit_entry, name='edit_entry'),
    path('new_topic_test/', views.new_topic_test, name='new_topic_test'),
]
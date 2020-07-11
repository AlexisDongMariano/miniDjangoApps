from django.contrib import admin
from blogs.models import BlogPost2, BlogComment2, Like

admin.site.register(BlogPost2)
admin.site.register(BlogComment2)
admin.site.register(Like)
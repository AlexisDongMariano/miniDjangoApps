from django.contrib import admin
from blogs.models import BlogPost, BlogComment


# title = models.CharField(max_length=300)
#     text = models.TextField()
#     date_added = models.DateTimeField(editable=False)
#     date_modified 


class BlogPostAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added',)
    fieldsets = [
        (None, {'fields': ['title']}),
        (None, {'fields': ['text']}),
        (None, {'fields': ['date_added']}),
        (None, {'fields': ['date_modified']}),
    ]


admin.site.register(BlogPost, BlogPostAdmin)
# admin.site.register(BlogPost)
admin.site.register(BlogComment)

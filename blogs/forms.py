from django import forms
from .models import BlogPost, BlogComment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title','text']
        labels = {'title':'', 'text':''}


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
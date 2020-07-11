from django import forms
from .models import BlogPost2, BlogComment2

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost2
        fields = ['title','text']
        labels = {'title':'', 'text':''}


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment2
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
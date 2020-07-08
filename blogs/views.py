from django.shortcuts import render, redirect
from .models import BlogPost, BlogComment
from .forms import BlogPostForm, BlogCommentForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    blogs = BlogPost.objects.order_by('-date_modified')
    context = {
        'blogs':blogs
    }
    return render(request, 'blogs/index.html', context)


def blog_details(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    comments = blog.blogcomment_set.order_by('date_added')

    if request.method != 'POST':
        form = BlogCommentForm()
    context = {
        'blog':blog,
        'comments':comments,
        'blog_id':blog_id,
        'form':form
    }
    return render(request, 'blogs/blog_details.html', context)


@login_required
def new_blog(request):
    """Add a new blog"""
    if request.method != 'POST':
        form = BlogPostForm()
    else:
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.owner = request.user
            # form_text = form.cleaned_data.get('text')
            form.save()
            return redirect('blogs:index')    
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)


@login_required
def edit_blog(request, blog_id):
    """Edit a blog"""
    blog = BlogPost.objects.get(id=blog_id)
    check_blog_owner(request, blog)
    if request.method != 'POST':
        form = BlogPostForm(instance=blog)
    else:
        form = BlogPostForm(data=request.POST, instance=blog)
        if form.is_valid():
            # form_text = form.cleaned_data.get('text')
            form.save()
            return redirect('blogs:blog-details', blog_id)    
    context = {'form':form, 'blog':blog}
    return render(request, 'blogs/edit_blog.html', context)


@login_required
def new_comment(request, blog_id):
    """Add a new blog"""
    blogpost = BlogPost.objects.get(id=blog_id)
    if request.method == 'POST':
        form = BlogCommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.blogpost = blogpost
            new_comment.save()
            # form_text = form.cleaned_data.get('text')
            
    return redirect('blogs:blog-details', blog_id)


def check_blog_owner(request, blog):
    if blog.owner != request.user:
        raise Http404
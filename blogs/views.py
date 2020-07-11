from django.shortcuts import render, redirect
from .models import BlogPost2, BlogComment2, Like
from .forms import BlogPostForm, BlogCommentForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index(request):
    blogs = BlogPost2.objects.order_by('-date_modified')
    context = {
        'blogs':blogs,
    }
    return render(request, 'blogs/index.html', context)


def blog_details(request, blog_id):
    blog = BlogPost2.objects.get(id=blog_id)
    comments = blog.blogcomment2_set.order_by('date_added')
    likes = Like.objects.filter(post=blog_id)

    liked = False
    if likes.filter(user=request.user).exists():
        liked = True
    else:
        liked = False

    if request.method != 'POST':
        form = BlogCommentForm()

    context = {
        'blog':blog,
        'comments':comments,
        'blog_id':blog_id,
        'form':form,
        'likes':likes,
        'liked':liked,
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
            new_form.ownerd = request.user
            # form_text = form.cleaned_data.get('text')
            form.save()
            return redirect('blogs2:index')    
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)


@login_required
def edit_blog(request, blog_id):
    """Edit a blog"""
    blog = BlogPost2.objects.get(id=blog_id)
    check_blog_owner(request, blog)
    if request.method != 'POST':
        form = BlogPostForm(instance=blog)
    else:
        form = BlogPostForm(data=request.POST, instance=blog)
        if form.is_valid():
            # form_text = form.cleaned_data.get('text')
            form.save()
            return redirect('blogs2:blog-details', blog_id)    
    context = {'form':form, 'blog':blog}
    return render(request, 'blogs/edit_blog.html', context)


@login_required
def new_comment(request, blog_id):
    """Add a new blog"""
    blogpost = BlogPost2.objects.get(id=blog_id)
    if request.method == 'POST':
        form = BlogCommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.ownerd = request.user
            new_comment.blogpost = blogpost
            new_comment.save()
            # form_text = form.cleaned_data.get('text')
            
    return redirect('blogs2:blog-details', blog_id)


def check_blog_owner(request, blog):
    if blog.ownerd != request.user:
        raise Http404


def blog_like(request, blog_id):
    blog = BlogPost2.objects.filter(id=blog_id).first()
    if request.method == 'POST':
        likes = Like.objects.filter(post=blog_id)
        instance = likes.filter(user=request.user)

        if instance.exists():
            instance.delete()
        else:
            new_like = Like(user=request.user, post=blog, value='Like')
            new_like.save()

    return redirect('blogs2:blog-details', blog_id)


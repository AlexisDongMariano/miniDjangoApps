from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    topics = Topic.objects.all()
    context = {
        'topics':topics,
        'request':request.META
    }
    return render(request, 'journals/index.html', context)

# MODIFIED BY DONG
@login_required
def topics(request):
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    #
    if request.method != 'POST':
        form = TopicForm()
    #
    context = {'topics':topics, 'form':form}
    return render(request, 'journals/topics.html', context)


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {'entries':entries,
                'topic':topic}
    return render(request, 'journals/topic.html', context)


def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # No data submitted, create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form_text = form.cleaned_data.get('text')
            # topics = Topic.objects.filter(text=form_text)
            topics_owner = Topic.objects.filter(text=form_text).filter(owner = request.user)
            # check if topic already exists, redirect to page if true
            if topics_owner:
                print('TRUEEEEEEEEEEEEEEEEEEEEEEEEEEE')
                # return redirect('journals:new_topic')
                form = TopicForm()
                error_message = f' Topic "{form_text}" already exists!'
                context = {'form': form,
                    'error_message': error_message}
                return render(request, 'journals/new_topic.html', context)
            else:
                new_topic.save()
                # form.save()
                # return HttpResponseRedirect(reverse('journals:topics'))
                return redirect('journals:topics')
            
    context = {'form': form}
    return render(request, 'journals/new_topic.html', context)


def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('journals:topic', topic_id)
            # return HttpResponseRedirect(reverse('journals:topic', args=[topic_id]))

    context = {'topic':topic, 'form':form}
    return render(request, 'journals/new_entry.html', context)


def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)
    
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('journals:topic', topic.id)
            # return HttpResponseRedirect(reverse('journals:topic', args=[topic.id]))
    
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'journals/edit_entry.html', context)


def new_topic_test(request):
    """add a new topic inside the topics page"""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form_text = form.cleaned_data.get('text')
            # topics = Topic.objects.filter(text=form_text)
            topics_owner = Topic.objects.filter(text=form_text).filter(owner = request.user)
            # check if topic already exists, redirect to page if true
            if topics_owner:
                print('TRUEEEEEEEEEEEEEEEEEEEEEEEEEEE')
                # return redirect('journals:new_topic')
                error_message = f' Topic "{form_text}" already exists!'
            else:
                new_topic.save()
                # form.save()
    return redirect('journals:topics')


def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404



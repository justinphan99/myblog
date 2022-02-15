from django.shortcuts import render, redirect
from .models import PostModel
from .forms import PostModelForm, PostUpdateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

@login_required
def index(request):
    posts = PostModel.objects.all()
    post_paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page = post_paginator.get_page(page_number)
    

    context = {
        'posts': posts,
        'page': page,
    }
    return render(request, 'blog/index.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('blog-index')
    else:
        form = PostModelForm()
    context = {
        'form': form
    }
    return render(request, 'blog/post_create.html', context)


@login_required
def post_detail(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == "POST":
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('blog-post-detail', pk=post.id)
    else:
        c_form = CommentForm()
    context = {
        'post': post,
        'c_form': c_form,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == "POST":
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog-post-detail', pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context ={
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)

@login_required
def post_delete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect('blog-index')
    context ={
        'post': post
    }
    return render(request, 'blog/post_delete.html', context)

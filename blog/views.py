from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *


CATEGORIES = Category.objects.order_by('pk')

# Create view list of posts
def post_list(request):
    # Get post list which published_date not empty
    # and order by published_date
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'post_list.html', {'posts': posts,
                                            'categories':CATEGORIES})

def post_detail(request, pk):
    user = auth.get_user(request)
    # Get post by primary_key(pk) or 404
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=pk).order_by('-created_date')
    post.views += 1
    post.comments = comments.count()
    post.save()
    #if this is a POST request need to process the form
    #create a form Comment:
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        #check valid:
        if form.is_valid():
            comment = form.save(commit=False)
            # user is auth
            if user.is_authenticated():
                comment.author = user.username
                comment.email = user.email
            # user not enter Name
            elif comment.author == '':
                comment.author = 'anonymous'
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=pk)
    return render(request, 'post_detail.html', {'post': post,
                                                'comments': comments,
                                                'form': form,
                                                'categories':CATEGORIES})

@login_required()
@render_to('post_edit.html')
def post_new(request):
    # Create form to add new posts
    #if this is a POST request need to process the form
    if request.method == 'POST':
        #create a form post:
        form = PostForm(request.POST)
        #check whether it's valid:
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        #if a GET (or any other method) create a blank form
        form = PostForm()
    return {'form': form,
            'categories':CATEGORIES}

def post_edit(request, pk):
    # Create form to edit post
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'post_edit.html', {'form': form,
                                                'categories':CATEGORIES})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    category = post.category.id
    post.delete()
    return redirect('blog.views.category_list', pk=category)

# Create views for comments
def comment_edit(request, pk):
    # Create form to edit comment
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('blog.views.post_detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)
        return render(request, 'comment_edit.html', {'form': form,
                                                'categories':CATEGORIES})

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post.id
    comment.delete()
    return redirect('blog.views.post_detail', pk=post)

# Create view list of catgory
# @render_to('')
def category_list(request, pk):
    # Get category by pk
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=pk, published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'post_list.html', {'posts': posts,
                                            'categories':CATEGORIES})

def category_new(request):
    # try post request
    form = CategoryForm(request.POST or None)
    if request.method == 'POST':
        #create a form category:
        #check whether it's valid:
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('blog.views.category_list', pk=category.pk)
    return render(request, 'category_edit.html', {'form': form,
                                                'categories':CATEGORIES})

# function for add likes
def add_like(request, pk):
    # try Post
    post = get_object_or_404(Post, pk=pk)
    # add like
    if ('pause' not in request.session) or (request.session['pk'] != pk):
        post.likes += 1
        post.save()
        request.session.set_expiry(60*5)
        request.session['pause'] = True
        request.session['pk'] = pk
    return redirect('blog.views.post_detail', pk=pk)

# auth
def login(request):
    # create form
    form = LoginForm(request.POST or None)
    # try post request
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('/')
            else:
                auth_error = 'User is not defined'
                return render(request, 'login.html', {'form':form, 'auth_error': auth_error, 'categories':CATEGORIES})
        else:
            return render(request, 'login.html', {'form':form, 'categories':CATEGORIES})
    else:
        return render(request, 'login.html', {'form':form, 'categories':CATEGORIES})

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        #create a form category:
        #check whether it's valid:
        if form.is_valid():
            # category = form.save(commit=False)
            form.save()
            return redirect('blog.views.login')
    return render(request, 'register.html', {'form': form,
                                            'categories':CATEGORIES})

def logout(request):
    auth.logout(request)
    return redirect('blog.views.login')


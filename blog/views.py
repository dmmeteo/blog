from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.core.paginator import Paginator
from .forms import *
from .models import *


CATEGORIES = Category.objects.all()

# Create view list of posts
@render_to('post_list.html')
def post_list(request, page_number=1):
    # Get post list which published_date not empty
    # and order by published_date
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    current_page = Paginator(posts, 3)
    return {'posts': current_page.page(page_number), 'categories':CATEGORIES}

@render_to('post_detail.html')
def post_detail(request, pk):
    user = auth.get_user(request)
    # Get post by primary_key(pk) or 404
    post = get_object_or_404(Post, pk=pk)
    # Get comments in post
    comments = Comment.objects.filter(post=pk).order_by('-created_date')
    post.comments = comments.count()
    # Add views to post
    # Create special key
    view_pk = 'view' + str(pk)
    if (view_pk not in request.session) or (request.session[view_pk] != pk):
        post.views += 1
        post.save()
        # Set expdate to session
        request.session.set_expiry(60*20)
        request.session[view_pk] = pk
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
    return {'post': post,
            'comments': comments,
            'form': form,
            'categories':CATEGORIES}

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

@login_required()
@render_to('post_edit.html')
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
        return {'form': form, 'categories':CATEGORIES}

@login_required()
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    category = post.category.id
    post.delete()
    return redirect('blog.views.category_list', pk=category)

# Create views for comments
@login_required()
@render_to('comment_edit.html')
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
        return {'form': form, 'categories':CATEGORIES}

@login_required()
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post.id
    comment.delete()
    return redirect('blog.views.post_detail', pk=post)

# Create view list of catgory
@render_to('post_list.html')
def category_list(request, pk, page_number=1):
    # Get category by pk
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=pk, published_date__lte=timezone.now()).order_by('-published_date')
    current_page = Paginator(posts, 3)
    return {'posts': current_page.page(page_number), 'category': category, 'categories':CATEGORIES}

@login_required()
@render_to('category_edit.html')
def category_new(request):
    #create a form category:
    form = CategoryForm(request.POST or None)
    # try post request
    if request.method == 'POST':
        #check whether it's valid:
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('blog.views.category_list', pk=category.pk)
    return {'form': form, 'categories':CATEGORIES}

@login_required()
@render_to('category_edit.html')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # try post request
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('blog.views.category_list', pk=pk)
    else:
        form = CategoryForm(instance=category)
        return {'form': form, 'categories':CATEGORIES}

@login_required()
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('/')

# function for add likes
def add_like(request, pk):
    # try Post
    post = get_object_or_404(Post, pk=pk)
    # create special key
    like_pk = 'like' + str(pk)
    # add like
    if (like_pk not in request.session) or (request.session[like_pk] != pk):
        post.likes += 1
        post.save()
        request.session.set_expiry(60*5)
        request.session[like_pk] = pk
    return redirect('blog.views.post_detail', pk=pk)

# auth
@render_to('login.html')
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
                return {'form':form, 'auth_error': auth_error, 'categories':CATEGORIES}
        else:
            return {'form':form, 'categories':CATEGORIES}
    else:
        return {'form':form, 'categories':CATEGORIES}

@render_to('register.html')
def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            auth.login(request, user)
            return redirect('/')
    return {'form': form, 'categories':CATEGORIES}

@login_required()
@render_to('password_change.html')
def password_change(request):
    form = PassChangeForm(user=request.user, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            message_success = True
            return {'message_success': message_success, 'categories':CATEGORIES}
        else:
            return {'form': form, 'categories':CATEGORIES}
    return {'form': form, 'categories':CATEGORIES}

def logout(request):
    auth.logout(request)
    return redirect('blog.views.login')

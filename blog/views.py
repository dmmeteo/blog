from annoying.decorators import render_to
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone


from .forms import CategoryForm, PostForm, CommentForm, LoginForm, RegisterForm, PassChangeForm
from .models import Category, Tag, Post, Comment


# Create view list of posts
@render_to('blog/post_list.html')
def post_list(request, page_number=1):
    # Get post list which published_date not empty
    # and order by published_date
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    current_page = Paginator(posts, 3)
    return {'posts': current_page.page(page_number),
            'categories': Category.objects.all(),
            'tags': Tag.objects.all()}


@render_to('blog/post_detail.html')
def post_detail(request, pk):
    user = auth.get_user(request)
    post = get_object_or_404(Post, pk=pk)
    tags = post.tags.all()
    comments = Comment.objects.filter(post=pk).order_by('-created_date')
    post.comments = comments.count()
    view_pk = 'view' + str(pk)

    if (view_pk not in request.session) or (request.session[view_pk] != pk):
        post.views += 1
        post.save()
        # Set expdate to session
        request.session.set_expiry(60 * 20)
        request.session[view_pk] = pk

    # create a form Comment:
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            # user is auth
            if user.is_authenticated():
                comment.author = user.username
                comment.email = user.email
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=pk)
    return {'tags': tags,
            'post': post,
            'comments': comments,
            'form': form,
            'categories': Category.objects.all()}


@login_required()
@render_to('blog/post_add.html')
def post_add(request, pk=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST or None, instance=post)
    else:
        form = PostForm(request.POST or None)

    if request.method == 'POST':
        new_tags = request.POST.getlist('tags')
        for tag in new_tags:
            try:
                Tag.objects.get(id=tag)
            except (ValueError, Tag.DoesNotExist):
                new_tag = Tag(name=tag)
                new_tag.save()
                new_tags[new_tags.index(tag)] = str(new_tag.pk)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            # update post if pk is None
            post.tags = new_tags
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    return {'form': form, 'categories': Category.objects.all()}


@login_required()
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    category = post.category.id
    post.delete()
    return redirect('blog.views.category_list', pk=category)


# Create view list by tag
@render_to('blog/post_list.html')
def tag_list(request, pk, page_number=1):
    # Get category by pk
    tag = get_object_or_404(Tag, pk=pk)
    posts = Post.objects.filter(tags=pk, published_date__lte=timezone.now()).order_by('-published_date')
    current_page = Paginator(posts, 3)
    return {'posts': current_page.page(page_number), 'tag': tag, 'categories': Category.objects.all()}


# Create views for comments
@login_required()
@render_to('blog/comment_edit.html')
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('blog.views.post_detail', pk=comment.post.id)
    return {'form': form, 'categories': Category.objects.all()}


@login_required()
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post.id
    comment.delete()
    return redirect('blog.views.post_detail', pk=post)


# Create view list of catgory
@render_to('blog/post_list.html')
def category_list(request, pk, page_number=1):
    # Get category by pk
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=pk, published_date__lte=timezone.now()).order_by('-published_date')
    current_page = Paginator(posts, 3)
    return {'posts': current_page.page(page_number), 'category': category, 'categories': Category.objects.all()}


@login_required()
@render_to('blog/category_add.html')
def category_add(request, pk=None):
    if pk:
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST or None, instance=category)
    else:
        form = CategoryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        category = form.save()
        return redirect('blog.views.category_list', pk=category.pk)

    return {'form': form, 'categories': Category.objects.all()}


@login_required()
def category_delete(request, pk):
    # TODO if delete some category - her posts change category "Without category"
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
        request.session.set_expiry(60 * 5)
        request.session[like_pk] = pk
    return redirect('blog.views.post_detail', pk=pk)


# auth
@render_to('blog/login.html')
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
                return {'form': form, 'auth_error': auth_error, 'categories': Category.objects.all()}
        else:
            return {'form': form, 'categories': Category.objects.all()}
    else:
        return {'form': form, 'categories': Category.objects.all()}


@render_to('blog/register.html')
def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            auth.login(request, user)
            return redirect('/')
    return {'form': form, 'categories': Category.objects.all()}


@login_required()
@render_to('blog/password_change.html')
def password_change(request):
    form = PassChangeForm(user=request.user, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            message_success = True
            return {'message_success': message_success, 'categories': Category.objects.all()}
        else:
            return {'form': form, 'categories': Category.objects.all()}
    return {'form': form, 'categories': Category.objects.all()}


def logout(request):
    auth.logout(request)
    return redirect('blog.views.login')

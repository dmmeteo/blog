from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import *
from .models import *
from django.contrib import auth


CATEGORIES = Category.objects.order_by('pk')

# Create view list of posts
def post_list(request):
	user = auth.get_user(request).username
	# Get post list which published_date not empty
	# and order by published_date
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'post_list.html', {'posts': posts,
											'categories':CATEGORIES,
											'username': user})

def post_detail(request, pk):
	user = auth.get_user(request)
	# Get post by primary_key(pk) or 404
	post = get_object_or_404(Post, pk=pk)
	comments = Comment.objects.filter(post=pk).order_by('-created_date')
	#if this is a POST request need to process the form
	if request.method == 'POST':
		#create a form comment:
		form = CommentForm(request.POST)
		#check valid:
		if form.is_valid():
			comment = form.save(commit=False)
			if user.is_authenticated():
				comment.author = user.username
				comment.email = user.email
			else:
				comment.author = 'anonymous'
			comment.post = post
			comment.save()
			return redirect('blog.views.post_detail', pk=pk)
	else:
		#if a GET (or any other method) create a blank form
		form = CommentForm()
	return render(request, 'post_detail.html', {'post': post,
												'comments': comments,
												'form': form,
												'categories':CATEGORIES,
												'username': user.username})

def post_new(request):
	user = auth.get_user(request).username
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
	return render(request, 'post_edit.html', {'form': form,
											'categories':CATEGORIES,
											'username': user})

def post_edit(request, pk):
	user = auth.get_user(request).username
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
												'categories':CATEGORIES,
												'username': user})

# Create view list of catgory
def category_list(request, pk):
	user = auth.get_user(request).username
	# Get category by pk
	category = get_object_or_404(Category, pk=pk)
	posts = Post.objects.filter(category=pk, published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'post_list.html', {'posts': posts,
											'categories':CATEGORIES,
											'username': user})

def category_new(request):
	user = auth.get_user(request).username
	# try post request
	if request.method == 'POST':
		#create a form category:
		form = CategoryForm(request.POST)
		#check whether it's valid:
		if form.is_valid():
			category = form.save(commit=False)
			category.save()
			return redirect('blog.views.category_list', pk=category.pk)
	else:
		#if a GET (or any other method) create a blank form
		form = CategoryForm()
	return render(request, 'category_edit.html', {'form': form,
												'categories':CATEGORIES,
												'username': user})

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
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			redirect('/')
		else:
			login_error = 'error'
			return render(request, 'login.html', {'categories':CATEGORIES,
												'login_error': login_error})
	else:
		return render(request, 'login.html', {'categories':CATEGORIES})

def logout(request):
	auth.logout(request)
	return redirect('/')


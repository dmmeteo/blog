from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import *
from .models import *

# Create view list of posts
def post_list(request):
	categories = Category.objects.order_by('-pk')
	# Get post list which published_date not empty
	# and order by published_date
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'post_list.html', {'posts': posts, 'categories':categories})

def category_list(request, pk):
	categories = Category.objects.order_by('-pk')
	category = get_object_or_404(Category, pk=pk)
	posts = Post.objects.filter(category=pk, published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'post_list.html', {'posts': posts, 'categories':categories})

def post_detail(request, pk):
	categories = Category.objects.order_by('-pk')
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
			comment.author = request.user
			comment.post = post
			comment.save()
			return redirect('blog.views.post_detail', pk=pk)
	else:
		#if a GET (or any other method) create a blank form
		form = CommentForm()
	return render(request, 'post_detail.html', {'post': post,
												'comments': comments,
												'form': form,
												'categories':categories})

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
	return render(request, 'post_edit.html', {'form': form})

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
		return render(request, 'post_edit.html', {'form': form})

def category_new(request):
	if request.method == 'POST':
		#create a form post:
		form = CategoryForm(request.POST)
		#check whether it's valid:
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			return redirect('/')
	else:
		#if a GET (or any other method) create a blank form
		form = CategoryForm()
	return render(request, 'category_edit.html', {'form': form})

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

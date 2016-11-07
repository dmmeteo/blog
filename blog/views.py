from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import *
from .models import *

# Create view list of posts
def post_list(request):
	# Get post list which published_date not empty
	# and order by published_date
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
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
	return render(request, 'post_detail.html', {'post': post,'comments': comments, 'form': form})

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

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm
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
	comments = Comment.objects.filter(post=pk)
	return render(request, 'post_detail.html', {'post': post, 'comments': comments})

def post_new(request):
	# Create form to add new posts
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('blog.views.post_detail', pk=post.pk)
	else:
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

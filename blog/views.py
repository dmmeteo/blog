from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post

# Create view list of posts
def post_list(request):
	# Get post list which published_date not empty
	# and order by published_date
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
	# Get post by primary_key(pk) or 404
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'post_detail.html', {'post': post})

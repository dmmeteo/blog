from django import forms
from .models import Category, Post, Comment

# Create Category form
class CategoryForm(forms.ModelForm):
	# create fields
	class Meta:
		model = Category
		fields = ['title', 'discript']

# Create Post form
class PostForm(forms.ModelForm):
	# create form name & fields
	class Meta:
		model = Post
		fields = ['category', 'title', 'text']

# Create Comment form
class CommentForm(forms.ModelForm):
	# create form comments
	class Meta:
		model = Comment
		fields = ['author', 'email', 'text']
		widgets = {
					'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
					'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
					'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Comment'}),
				}


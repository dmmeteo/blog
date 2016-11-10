from django import forms
from .models import Category, Post, Comment
from django.contrib.auth.models import User

# Create Category form
class CategoryForm(forms.ModelForm):
	# create fields
	class Meta:
		model = Category
		fields = ['title', 'discript']
		widgets = {
					'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
					'discript': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comment'}),
				}

# Create Post form
class PostForm(forms.ModelForm):
	# create form name & fields
	class Meta:
		model = Post
		fields = ['category', 'title', 'text']
		widgets = {
					'category': forms.Select(attrs={'class': 'form-control'}),
					'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
					'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Discription'}),
				}

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

# Create auth
class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class RegisterForm(forms.ModelForm):
    model = User
    fields = ['username','password1','password2']

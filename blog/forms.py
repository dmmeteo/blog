from django import forms
from .models import Category, Post, Comment
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


# Create Category form
class CategoryForm(forms.ModelForm):

    # create fields
    class Meta:
        model = Category
        fields = ['title', 'discript']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'discript': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comment'}),
        }

    def clean(self):
        data = self.cleaned_data
        if data['title'].isdigit():
            self.add_error('title', forms.ValidationError('Title must be a string'))
        return data


# Create Post form
class PostForm(forms.ModelForm):
    # create form name & fields
    class Meta:
        model = Post
        fields = ['category', 'tags', 'title', 'text']
        widgets = {
            'category': forms.Select(
                attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(
                attrs={'id': 'select-tags'}),
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Discription'}),
        }

    def clean(self):
        data = self.cleaned_data
        try:
            data['tags']
        except KeyError:
            data['tags'] = ''
        if data['title'].isdigit() or data['title'] == '':
            self.add_error('title', forms.ValidationError('Title must be a string'))
        if data['text'] == '':
            self.add_error('text', forms.ValidationError('Post must be not empty and be string'))
        return data


# Create Comment form
class CommentForm(forms.ModelForm):
    # create form comments
    class Meta:
        model = Comment
        fields = ['author', 'email', 'text']
        widgets = {
            'author': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Comment'}),
        }

    def clean(self):
        data = self.cleaned_data
        if data['author'] == '':
            data['author'] = 'anonymous'
        return data


# Create auth
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Password again'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }


class PassChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old password'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password again'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

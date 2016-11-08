from django.contrib import admin
from .models import Category, Post, Comment

# class for category in admin
class CategoryAdmin(admin.ModelAdmin):
	fields = ['title', 'discript']

# class for comments in admin
class PostInline(admin.StackedInline):
	model = Comment
	extra = 2

# class for views fields in admin
class PostAdmin(admin.ModelAdmin):
	fields = ['category', 'author', 'title', 'text', 'created_date', 'published_date']
	inlines = [PostInline]
	list_filter = ['created_date']

# Register models
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)

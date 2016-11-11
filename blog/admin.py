from django.contrib import admin
from .models import Category, Post, Tag, Comment

# class for category in admin
class CategoryAdmin(admin.ModelAdmin):
	fields = ['title', 'discript']

# class for comments in admin
class CommentAdmin(admin.ModelAdmin):
	fields = ['author','text','email','post','created_date']
	list_filter = ['created_date','post']

class PostInline(admin.StackedInline):
	model = Comment
	extra = 2

# class for views fields in admin
class PostAdmin(admin.ModelAdmin):
	fields = ['category', 'author', 'tags', 'title', 'text', 'created_date', 'published_date']
	inlines = [PostInline]
	list_filter = ['created_date']

# Register models
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)

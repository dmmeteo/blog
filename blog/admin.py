from django.contrib import admin
from .models import *

# class for comments in admin
class PostInline(admin.StackedInline):
	model = Comment
	extra = 2

# class for views fields in admin
class PostAdmin(admin.ModelAdmin):
	fields = ['author','title','text','created_date','published_date']
	inlines = [PostInline]
	list_filter = ['created_date']

# Register models
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

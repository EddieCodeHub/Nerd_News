from django.contrib import admin
from .models import News_Post, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(News_Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on', 'author')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

# Register your models here.
admin.site.register(Comment)
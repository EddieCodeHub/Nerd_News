from django.contrib import admin
from .models import News_Post, Comment



# Register your models here.
admin.site.register(News_Post)
admin.site.register(Comment)
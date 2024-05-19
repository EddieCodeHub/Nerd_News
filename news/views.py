from django.shortcuts import render
from django.views import generic
from .models import News_Post, Comment


# Create your views here.
class News_Post_List(generic.ListView):
    queryset = News_Post.objects.all()
    template_name = "news_post_list.html"

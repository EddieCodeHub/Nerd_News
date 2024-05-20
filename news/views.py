from django.shortcuts import render
from django.views import generic
from .models import News_Post, Comment


# Create your views here.
class news_post_list(generic.ListView):
    queryset = News_Post.objects.all()
    template_name = "news/index.html"
    paginate_by = 3
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import News_Post, Comment


# Create your views here.
class news_post_list(generic.ListView):
    queryset = News_Post.objects.all()
    template_name = "news/index.html"
    paginate_by = 3


def post_detail(request, slug):
    """
    Display an individual :model:`news.News_Post`.

    **Context**

    ``post``
        An instance of :model:`news.News_Post`.

    **Template:**

    :template:`news/post_detail.html`
    """

    queryset = News_Post.objects.all()
    post = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "news/post_detail.html",
        {"News_Post": post},
    )
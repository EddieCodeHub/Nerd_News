from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import News_Post
from .forms import CommentForm


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
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted successfully.'
            )

    comment_form = CommentForm()


    return render(
        request,
        "news/post_detail.html",
        {
            "News_Post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )
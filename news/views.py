from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum, Case, When, IntegerField, Count
from django.views.generic import ListView   
from .models import News_Post, Comment, Vote
from .forms import CommentForm, NewsPostForm


# Create your views here.
class news_post_list(generic.ListView):
    queryset = News_Post.objects.all()
    template_name = "news/index.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsPostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = NewsPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False, user=request.user)
            post.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Post added successfully.'
            )
            return redirect('home')
        return self.get(request, *args, **kwargs)
    
    def get_queryset(self):
        return News_Post.objects.filter(status=1).annotate(comment_count=Count('comments'))


def post_detail(request, slug):
    """
    Display an individual :model:`news.News_Post`.

    **Context**

    ``post``
        An instance of :model:`news.News_Post`.

    **Template:**

    :template:`news/post_detail.html`
    """

    queryset = News_Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = Comment.objects.filter(post=post).annotate(
        upvotes=Sum(Case(When(votes__value=1, then=1), output_field=IntegerField())),
        downvotes=Sum(Case(When(votes__value=-1, then=1), output_field=IntegerField())),
    ).order_by('-upvotes')
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


def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = News_Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = News_Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

def add_post(request):
    if request.method == "POST":
        form = NewsPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False, user=request.user)
            post.author = request.user
            post.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Post added successfully.'
            )
            return redirect('home')
        else:
            print(form.errors)
    return redirect('home')
        

def post_edit(request, slug):
    """
    view to edit posts
    """
    post = get_object_or_404(News_Post, slug=slug)
    if request.method == "POST":
        post_form = NewsPostForm(data=request.POST, instance=post)

        if post_form.is_valid() and post.author == request.user:
            post = post_form.save()
            messages.add_message(request, messages.SUCCESS, 'Post Updated!')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating post!')
            return render(request, 'news/index.html', {'form': post_form})
    else:
        post_form = NewsPostForm(instance=post)
    return render(request, 'news/index.html', {'form': post_form})



def post_delete(request, slug):
    """
    view to delete post
    """
    post = get_object_or_404(News_Post, slug=slug)
    if post.author == request.user:
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Post deleted!')
        return redirect('home')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own posts!')
        return redirect('home', args=[slug])


def vote(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    value = int(request.POST['value'])
    post = get_object_or_404(News_Post, id=comment.post.id)

    vote, created = Vote.objects.get_or_create(
        user=request.user,
        comment=comment,
        defaults={'value': value},
    )

    if not created and vote.value != value:
        vote.value = value
        vote.save()

    return redirect('post_detail', slug=post.slug)
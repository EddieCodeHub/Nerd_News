from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator



STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.
class News_Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="News_posts")
    content = models.TextField()
    summary = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=1)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return f"{self.title} written by {self.author}"
    
    def save(self, *args, **kwargs):
        if not self.summary:
            self.summary = Truncator(self.content).chars(100)
        super(News_Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(News_Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def vote_total(self):
       return self.votes.aggregate(total=models.Sum('value'))['total'] or 0


    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    

class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1

    VOTE_CHOICES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    value = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.value} by {self.user} on {self.comment}"
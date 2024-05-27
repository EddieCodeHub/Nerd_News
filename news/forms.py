from django import forms
from django.utils.text import slugify
from .models import Comment, News_Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class NewsPostForm(forms.ModelForm):
    class Meta:
        model = News_Post
        fields = ['title', 'content']  # Removed 'author' from fields

    def save(self, commit=True, user=None):
        instance = super(NewsPostForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if user:
            instance.author = user
        if commit:
            instance.save()
        return instance
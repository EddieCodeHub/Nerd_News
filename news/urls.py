from . import views
from django.urls import path


urlpatterns = [
     path('', views.news_post_list.as_view(), name='home'),
     path('<slug:slug>/', views.post_detail, name='post_detail'),
     path('<slug:slug>/edit_comment/<int:comment_id>',
          views.comment_edit, name='comment_edit'),
     path('<slug:slug>/delete_comment/<int:comment_id>',
          views.comment_delete, name='comment_delete'),
     path('vote/<int:comment_id>/', views.vote, name='vote'),
     path('delete_post/<slug>', views.post_delete, name='post_delete'),
]
from . import views
from django.urls import path


urlpatterns = [
    path('', views.news_post_list.as_view(), name='home'),
]
from . import views
from django.urls import path


urlpatterns = [
    path('', views.News_Post_List.as_view(), name='home'),
]
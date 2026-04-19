from django.urls import path
from .views import create_comment, create_post

urlpatterns = [
    path("create-post/", create_post),
    path("create-comment/", create_comment),
]
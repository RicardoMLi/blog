from django.urls import path

from .views import CommentView


urlpatterns = [
    path('add/', CommentView.as_view(), name='add_comment'),
]
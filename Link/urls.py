from django.urls import path

from .views import LinksView


urlpatterns = [
    path('', LinksView.as_view(), name='link'),
]
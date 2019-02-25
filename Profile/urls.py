from django.urls import path

from .views import AboutMeView

urlpatterns = [
    path('', AboutMeView.as_view(), name='about'),
]
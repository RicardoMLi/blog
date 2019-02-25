from django.urls import path

from . import views
from Profile.views import AboutMeView

urlpatterns = [
    path('mydaily/', views.MyDailyView.as_view()),
    path('mydaily/<str:router>/', views.MyDailyExtendView.as_view()),
    path('technology/', views.TechnologyView.as_view()),
    path('technology/<str:router>/', views.TechnologyExtendView.as_view()),
    path('message/',views.MessageView.as_view(), name='message'),
    path('donate/', views.DonationView.as_view(), name='donate'),
    path('share/', views.ShareView.as_view()),
    path('share/<str:router>', views.ShareExtendView.as_view()),
    path('profile/', AboutMeView.as_view()),
    path('find_parent/', views.FindParentView.as_view(), name='find_parent'),
]
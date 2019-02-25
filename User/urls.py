from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('check_name/', views.CheckNameView.as_view(), name='check_name'),
    path('check_email/', views.CheckEmailView.as_view(), name='check_email'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register_success/', views.RegisterSuccessView.as_view(), name='register_success'),
    path('active/<str:active_code>/', views.ActiveUserView.as_view(),name='active_user'),

]
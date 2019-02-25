"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', include('haystack.urls')),
    path('xadmin/', xadmin.site.urls),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('user/',include('User.urls'), name='user'),
    path('profile/', include('Profile.urls'), name='profile'),
    path('blog/', include('Blog.urls'), name='blog'),
    path('category/',include('Category.urls'), name='category'),
    path('comment/',include('Comment.urls'), name='comment'),
    path('link/', include('Link.urls'), name='links')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
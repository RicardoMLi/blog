from django.urls import path

from .views import BlogView, LikeAddView, TagView, BlogWithDateView, HistoryBlogsView, AllTagsView, ShareBlogView

urlpatterns = [
    path('<int:blog_id>/', BlogView.as_view(), name='blog_detail'),
    path('history/', HistoryBlogsView.as_view(), name='history'),
    path('date/<int:year>/<int:month>',BlogWithDateView.as_view(),name='get_blogs_with_date'),
    path('add_like/', LikeAddView.as_view(), name='add_like'),
    path('tag/<str:tag_name>', TagView.as_view(), name='tag'),
    path('all_tags/', AllTagsView.as_view(), name='all_tags'),
    path('share/', ShareBlogView.as_view(), name='share_blog'),
]
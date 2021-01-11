from django.urls import path 

from .views import *

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    # path('', PostListView.as_view(), name='posts_list_url'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post-detail'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name='post-update'),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name='post-delete'),

]
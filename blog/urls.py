from django.urls import path 

from .views import *

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('post/create/', PostCreate.as_view(), name='post-create'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post-detail'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name='post-update'),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name='post-delete'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<str:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),

    # path('', PostListView.as_view(), name='blog-home'),
    # path('about/',views.about, name='blog-about'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/del/', PostDeleteView.as_view(), name='post-delete'),
    # path('user/<str:username>/follows', FollowsListView.as_view(), name='user-follows'),
    # path('user/<str:username>/followers', FollowersListView.as_view(), name='user-followers'),
    # path('post/<int:postid>/preference/<int:userpreference>', postpreference, name='postpreference'),
    # path('l/', include(router.urls)),

]
from django.urls import path
from . import views

urlpatterns = [
    path('my-models/', views.user_feed_list, name="user-feed-list"), 
    path("explore/", views.getExplorePosts, name="posts"),
    path("post/<str:pk>/", views.getPost, name="post"),
    path("create/", views.createPost, name="create-post"),
    path("delete/<str:post_id>/", views.deletePost, name="delete-post"),
    path("like/<str:post_id>/", views.like_post, name="like-post"),
    path("isliked/<str:post_id>/", views.getIsPostLiked, name="isliked"),

    path("feed/", views.user_feed, name="user-feed"),
    path("<str:username>/posts/", views.getCurrUserPosts, name="curr-user-posts"),

    path("<pid>/comments/", views.getPostComment, name="comment"),
    path("create-comment/", views.setPostComment, name="set-comment"),
    path("comments/<str:comment_id>/delete/", views.deletePostComment, name="set-comment"),


]



from django.urls import path

from articles.views.articles_views import ArticlesCreateViews, ArticlesViews, \
    ArticleLikesViews, ArticleCommentsViews, TagViews, ArticleCommentsRepliesViews, UserArticlesViews

urlpatterns = [
    path('', ArticlesCreateViews.as_view(), name='articles-create'),
    path('<str:username>/', UserArticlesViews.as_view(), name='user-articles'),
    path('<str:slug>/', ArticlesViews.as_view(), name='articles-actions'),

    path('<int:pk>/likes/set/', ArticleLikesViews.as_view(), name='articles-like'),

    path('<int:pk>/comments/', ArticleCommentsViews.as_view(), name='articles-comment'),
    path('<int:pk>/comments/<int:comment_id>/replies/', ArticleCommentsRepliesViews.as_view(), name='comment-replies'),
    path('tags/', TagViews.as_view(), name='tags-create'),
]

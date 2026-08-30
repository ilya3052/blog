from django.urls import path

from articles.views.articles_views import ArticlesListCreateViews, ArticlesViews, \
    ArticleLikesViews, ArticleCommentsViews, TagViews, ArticleCommentsRepliesViews, UserArticlesViews, \
    ArticleBookmarksViews

urlpatterns = [
    path('tags/', TagViews.as_view(), name='tags-create'),

    path('', ArticlesListCreateViews.as_view(), name='articles-list-create'),
    path('user/<str:username>/', UserArticlesViews.as_view(), name='user-articles'),
    path('slug/<str:slug>/', ArticlesViews.as_view(), name='article-detail-info'),

    path('<int:pk>/bookmark/', ArticleBookmarksViews.as_view(), name='article-bookmarks'),

    path('<int:pk>/like/', ArticleLikesViews.as_view(), name='articles-like'),

    path('<int:pk>/comment/', ArticleCommentsViews.as_view(), name='articles-comment'),
    path('<int:pk>/comment/<int:comment_id>/replies/', ArticleCommentsRepliesViews.as_view(), name='comment-replies'),
]

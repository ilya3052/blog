from django.urls import path

from articles.views.articles_views import ArticlesCreateViews, ArticlesViews, \
    ArticleLikesViews, ArticleCommentsViews, TagViews

urlpatterns = [
    path('', ArticlesCreateViews.as_view(), name='articles-create'),
    path('<int:pk>/', ArticlesViews.as_view(), name='articles-get'),

    path('<int:pk>/likes/set/', ArticleLikesViews.as_view(), name='articles-like'),
    # path('<int:pk>/likes/all/', ArticleLikesRetrieveViews.as_view(), name='articles-like-all'), #необходимо ли?

    path('<int:pk>/comments/', ArticleCommentsViews.as_view(), name='articles-comment'),

    path('tags/', TagViews.as_view(), name='tags-create'),
]

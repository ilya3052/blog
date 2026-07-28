from django.urls import path

from articles.views.articles_views import ArticlesCreateViews, TagCreateViews, TagRetrieveAll, ArticlesViews, \
    ArticleLikesViews, ArticleCommentsViews

urlpatterns = [
    path('', ArticlesCreateViews.as_view(), name='articles-create'),
    path('<int:pk>/', ArticlesViews.as_view(), name='articles-get'),

    path('<int:pk>/likes/set/', ArticleLikesViews.as_view(), name='articles-like'),
    # path('<int:pk>/likes/all/', ArticleLikesRetrieveViews.as_view(), name='articles-like-all'), #необходимо ли?

    path('<int:pk>/comment/send/', ArticleCommentsViews.as_view(), name='articles-comment'),

    path('tags/', TagCreateViews.as_view(), name='tags-create'),
    path('tags/all/', TagRetrieveAll.as_view(), name='tags-all'),
]
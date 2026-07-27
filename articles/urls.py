from django.urls import path

from articles.views.articles_views import ArticlesCreateViews, TagCreateViews, TagRetrieveAll, ArticlesViews

urlpatterns = [
    path('', ArticlesCreateViews.as_view(), name='articles-create'),
    path('<int:pk>/', ArticlesViews.as_view(), name='articles-get'),

    path('tags/', TagCreateViews.as_view(), name='tags-create'),
    path('tags/all/', TagRetrieveAll.as_view(), name='tags-all'),
]
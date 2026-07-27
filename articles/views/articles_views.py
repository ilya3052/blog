from rest_framework import generics
from rest_framework.permissions import AllowAny

from articles.models import Article, Tag
from articles.seriaizers.articles_serializers import ArticleSerializer, TagSerializer


class ArticlesCreateViews(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]


class ArticlesViews(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        queryset = Article.objects.filter(pk=self.kwargs['pk'])
        return queryset

    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'


class TagCreateViews(generics.CreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class TagRetrieveAll(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

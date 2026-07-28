from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from articles.models import Article, Tag, ArticleComments, ArticleLikes
from articles.seriaizers.articles_serializers import ArticleSerializer, TagSerializer, ArticleCommentsSerializer, \
    ArticleLikesSerializer


class ArticlesCreateViews(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


class ArticlesViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Article.objects.prefetch_related('likes__user').prefetch_related('comments').filter(
            pk=self.kwargs['pk'])
        return queryset

    lookup_field = 'pk'


class TagCreateViews(generics.CreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class TagRetrieveAll(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class ArticleCommentsViews(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        article_id = self.kwargs['pk']
        request.data['article'] = article_id
        request.data['author_id'] = request.data.pop('user')
        return super().create(request, *args, **kwargs)

    serializer_class = ArticleCommentsSerializer
    permission_classes = [IsAuthenticated]


class ArticleCommentsRetrieveViews(generics.ListAPIView):
    serializer_class = ArticleCommentsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = ArticleComments.objects.select_related('author').filter(article_id=self.kwargs['pk'])
        return queryset


class ArticleLikesViews(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        article_id = self.kwargs['pk']
        user_id = request.data.get('user')
        request.data['article'] = article_id

        if (instance := ArticleLikes.objects.filter(article_id=article_id, user_id=user_id)).exists():
            instance.delete()
            return Response({"detail": "Лайк снят"}, status=status.HTTP_204_NO_CONTENT)

        return super().create(request, *args, **kwargs)

    serializer_class = ArticleLikesSerializer
    permission_classes = [IsAuthenticated]

# class ArticleLikesRetrieveViews(generics.ListAPIView):
#     serializer_class = ArticleLikesSerializer
#     permission_classes = [AllowAny]
#     pagination_class = None
#
#     def get_queryset(self):
#         queryset = ArticleLikes.objects.select_related('user').filter(article_id=self.kwargs['pk'])
#         return queryset

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from articles.models import Article, Tag, ArticleComments, ArticleLikes
from articles.permissions import IsOwner, ReadOnly
from articles.seriaizers.articles_serializers import ArticleSerializer, TagSerializer, ArticleCommentsSerializer, \
    ArticleLikesSerializer


class ArticlesCreateViews(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['author_id'] = request.user.id
        return super().create(request, *args, **kwargs)


class ArticlesViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permissions = [IsAuthenticated]
        elif self.request.method in ('PATCH', 'DELETE'):
            permissions = [IsAuthenticated, IsOwner]
        else:
            permissions = [ReadOnly]
        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Article.objects.prefetch_related('likes__user').prefetch_related('comments').filter(
            pk=self.kwargs['pk'])
        return queryset

    lookup_field = 'pk'


class TagViews(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ArticleCommentsViews(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = ArticleComments.objects.select_related('author').filter(article_id=self.kwargs['pk'])
        return queryset

    def create(self, request, *args, **kwargs):
        article_id = self.kwargs['pk']
        request.data['article'] = article_id
        request.data['author_id'] = request.user.id
        return super().create(request, *args, **kwargs)

    serializer_class = ArticleCommentsSerializer
    permission_classes = [IsAuthenticated]


class ArticleLikesViews(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        article_id = self.kwargs['pk']
        request.data['article'] = article_id
        request.data['user_id'] = request.user.id
        if (instance := ArticleLikes.objects.filter(article_id=article_id, user_id=request.user.id)).exists():
            instance.delete()
            return Response({"detail": "Лайк снят"}, status=status.HTTP_204_NO_CONTENT)

        return super().create(request, *args, **kwargs)

    serializer_class = ArticleLikesSerializer
    permission_classes = [IsAuthenticated]

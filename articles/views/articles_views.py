from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from articles.models import Article, Tag, ArticleComments, ArticleLikes
from articles.permissions import IsArticleOwner, ReadOnly
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
            permissions = [IsAuthenticatedOrReadOnly]
        elif self.request.method in ('PATCH', 'DELETE'):
            permissions = [IsAuthenticated, IsArticleOwner]
        else:
            permissions = [ReadOnly]
        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Article.objects.select_related('author').prefetch_related('likes__user').filter(
            slug=self.kwargs['slug'])
        return queryset

    lookup_field = 'slug'


class TagViews(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ArticleCommentsViews(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            permissions = [IsAuthenticatedOrReadOnly]
        elif self.request.method in ('POST',):
            permissions = [IsAuthenticated]
        else:
            permissions = [ReadOnly]
        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = ArticleComments.objects.select_related('author').filter(article_id=self.kwargs['pk'], parent=None)
        return queryset

    def create(self, request, *args, **kwargs):
        article_id = self.kwargs['pk']
        request.data['article'] = article_id
        request.data['author_id'] = request.user.id
        return super().create(request, *args, **kwargs)

    serializer_class = ArticleCommentsSerializer


class ArticleCommentsRepliesViews(generics.RetrieveAPIView):
    serializer_class = ArticleCommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        article = Article.objects.filter(pk=self.kwargs['pk']).first()
        if not article:
            return Response({'detail': 'Статья не найдена'}, status=status.HTTP_404_NOT_FOUND)

        comment: ArticleComments = ArticleComments.objects.filter(pk=self.kwargs['comment_id']).first()
        if not comment:
            return Response({'detail': 'Комментарий не найден'}, status=status.HTTP_404_NOT_FOUND)

        if comment.get_root().article != article:
            return Response({'detail': 'Некорректная ветка комментариев'}, status=status.HTTP_404_NOT_FOUND)

        replies = comment.get_children()
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = [IsAuthenticatedOrReadOnly]


class MyArticlesViews(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Article.objects.prefetch_related('likes__user').filter(author=self.request.user)

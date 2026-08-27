from django.db.models import Exists, OuterRef
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from articles.exceptions import UserNotFoundError
from articles.models import Article, Tag, ArticleComments, ArticleLikes, ArticleBookmarks
from articles.permissions import ReadOnly, IsArticleOwner
from articles.seriaizers.articles_serializers import ArticleCreateSerializer, TagSerializer, \
    ArticleCommentsSerializer, \
    ArticleLikesSerializer, ArticleDetailInfoSerializer, ArticleShortInfoSerializer, ArticleBookmarksSerializer
from users.models import CustomUser


class ArticlesCreateViews(generics.CreateAPIView):
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)


class ArticlesViews(generics.RetrieveUpdateAPIView):
    serializer_class = ArticleDetailInfoSerializer
    permission_classes = [ReadOnly]

    def get_permissions(self):
        if self.request.method == 'PATCH':
            perm = [IsAuthenticated, IsArticleOwner]
        else:
            perm = [ReadOnly]
        return [perm() for perm in perm]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Article.objects
            .annotate(
                is_liked=Exists(
                    ArticleLikes.objects.filter(
                        article=OuterRef('pk'),
                        user=user
                    )
                ),
                is_bookmarked=Exists(
                    ArticleBookmarks.objects.filter(
                        article=OuterRef('pk'),
                        user=user
                    )
                )
            )
            .select_related('author')
            .prefetch_related('comments')
            .prefetch_related('likes')
            .prefetch_related('unique_views')
            .filter(slug=self.kwargs['slug']))
        return queryset

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    lookup_field = 'slug'


class ArticlesListView(generics.ListAPIView):  # заготовка для будущей ленты
    serializer_class = ArticleShortInfoSerializer
    permission_classes = [ReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Article.objects
            .annotate(
                is_liked=Exists(
                    ArticleLikes.objects.filter(
                        article=OuterRef('pk'),
                        user=user
                    )
                ),
                is_bookmarked=Exists(
                    ArticleBookmarks.objects.filter(
                        article=OuterRef('pk'),
                        user=user
                    )
                )
            )
            .select_related('author')
            .prefetch_related('comments')
            .prefetch_related('likes')
            .prefetch_related('unique_views'))
        return queryset


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

        comment: ArticleComments = ArticleComments.objects.select_related('article').filter(
            pk=self.kwargs['comment_id']).first()
        if not comment:
            return Response({'detail': 'Комментарий не найден'}, status=status.HTTP_404_NOT_FOUND)

        if comment.get_root().article != article:
            return Response({'detail': 'Некорректная ветка комментариев'}, status=status.HTTP_404_NOT_FOUND)

        replies = comment.get_children()
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleBookmarksViews(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        article_id = self.kwargs['pk']
        request.data['article'] = article_id
        request.data['user_id'] = request.user.id
        if (instance := ArticleBookmarks.objects.filter(article_id=article_id, user_id=request.user.id)).exists():
            instance.delete()
            return Response({"detail": "Статья удалена из избранного"}, status=status.HTTP_204_NO_CONTENT)

        return super().create(request, *args, **kwargs)

    serializer_class = ArticleBookmarksSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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


class UserArticlesViews(generics.ListAPIView):
    serializer_class = ArticleDetailInfoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def get_queryset(self):
        user = self.request.user
        author = CustomUser.objects.filter(username=self.kwargs.get('username')).first()
        if not author:
            raise UserNotFoundError
        return (Article.objects
                .annotate(
            is_liked=Exists(
                ArticleLikes.objects.filter(
                    article=OuterRef('pk'),
                    user=user
                )
            ),
            is_bookmarked=Exists(
                ArticleBookmarks.objects.filter(
                    article=OuterRef('pk'),
                    user=user
                )
            )
        )
                .select_related('author')
                .prefetch_related('comments')
                .prefetch_related('likes')
                .prefetch_related('unique_views')
                .filter(author=author))

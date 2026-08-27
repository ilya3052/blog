from rest_framework import serializers

from articles.models import Article, Tag, ArticleComments, ArticleLikes, ArticleBookmarks
from users.models import CustomUser
from users.serializers.user_serializer import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ArticleCommentsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='author',
        write_only=True
    )

    class Meta:
        model = ArticleComments
        fields = ('id', 'content', 'added_at', 'author', 'article', 'author_id', 'parent')
        extra_kwargs = {'article': {'write_only': True}}


class ArticleBookmarksSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = ArticleBookmarks
        fields = ('user', 'article', 'user_id')
        extra_kwargs = {'article': {'write_only': True}}


class ArticleLikesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = ArticleLikes
        fields = ('user', 'article', 'user_id')
        extra_kwargs = {'article': {'write_only': True}}


class ArticleStatsSerializer(serializers.Serializer):
    likes_count = serializers.SerializerMethodField(read_only=True)
    views_count = serializers.SerializerMethodField(read_only=True)
    unique_views_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    reading_time = serializers.SerializerMethodField(read_only=True)

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_views_count(self, obj):
        return obj.views

    def get_unique_views_count(self, obj):
        return obj.unique_views.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_reading_time(self, obj):
        return obj.reading_time


class ArticleCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True
    )

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'slug', 'created_at', 'tags', 'author_id')


class ArticleBaseSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    stats = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.BooleanField()
    is_bookmarked = serializers.BooleanField()

    def get_stats(self, obj):
        return ArticleStatsSerializer(obj).data


class ArticleShortInfoSerializer(ArticleBaseSerializer):
    content = serializers.SerializerMethodField(read_only=True)

    def get_content(self, obj):
        if not hasattr(obj, 'content'):
            return ''
        return f'{obj.content[:150]}...'

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'slug', 'created_at', 'tags', 'author', 'stats', 'is_liked',
                  'is_bookmarked')


class ArticleDetailInfoSerializer(ArticleBaseSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'slug', 'created_at', 'updated_at', 'status', 'tags', 'author', 'stats',
                  'is_liked', 'is_bookmarked')

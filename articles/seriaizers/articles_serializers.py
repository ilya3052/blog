from rest_framework import serializers

from articles.models import Article, Tag, ArticleComments, ArticleLikes, ArticleBookmarks
from articles.signals import article_published
from users.models import CustomUser
from users.serializers.user_serializer import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ArticleUserMixinSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        fields = ('user', 'article', 'user_id')
        extra_kwargs = {'article': {'write_only': True}}


class ArticleCommentsSerializer(ArticleUserMixinSerializer, serializers.ModelSerializer):
    class Meta(ArticleUserMixinSerializer.Meta):
        model = ArticleComments
        fields = ArticleUserMixinSerializer.Meta.fields + ('id', 'content', 'added_at', 'parent')


class ArticleBookmarksSerializer(ArticleUserMixinSerializer, serializers.ModelSerializer):
    class Meta(ArticleUserMixinSerializer.Meta):
        model = ArticleBookmarks


class ArticleLikesSerializer(ArticleUserMixinSerializer, serializers.ModelSerializer):
    class Meta(ArticleUserMixinSerializer.Meta):
        model = ArticleLikes


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
    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        instance = super().update(instance, validated_data)
        if old_status != 'PUBLISHED' and new_status == 'PUBLISHED':
            article_published.send(sender=Article, instance=instance)
        return instance

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'slug', 'created_at', 'updated_at', 'status', 'tags', 'author', 'stats',
                  'is_liked', 'is_bookmarked')

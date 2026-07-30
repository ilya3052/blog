from rest_framework import serializers

from articles.models import Article, Tag, ArticleComments, ArticleLikes
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
        fields = ('id', 'content', 'added_at', 'author', 'article', 'author_id')
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


class ArticleSerializer(serializers.ModelSerializer):
    likes = ArticleLikesSerializer(many=True, read_only=True)
    comments = ArticleCommentsSerializer(many=True, read_only=True)

    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True
    )
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        write_only=True,
        source='author'
    )

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'tags', 'tags_ids', 'likes', 'comments', 'author', 'author_id')

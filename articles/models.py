from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='articles')
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'articles'


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'


class ArticleComments(models.Model):
    content = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey('Article', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        db_table = 'article_comments'


class ArticleLikes(models.Model):
    pk = models.CompositePrimaryKey('article_id', 'user_id')

    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = 'article_likes'


class Notifications(models.Model):
    STATUS = {"UNREAD": "UNREAD", "READ": "READ"}
    recipient = models.ForeignKey(user, on_delete=models.CASCADE, related_name='notifications')
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='notifications')
    status = models.CharField(choices=STATUS.items(), max_length=6, default=STATUS["UNREAD"])
    publication_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'notifications'

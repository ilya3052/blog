from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from unidecode import unidecode

user = get_user_model()

READING_SPEED_IN_WORDS_PER_MINUTE = 200


class Article(models.Model):
    STATUS = {"PUBLISHED": "PUBLISHED", "DRAFT": "DRAFT"}
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='articles')
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='articles')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)
    status = models.CharField(choices=STATUS.items(), max_length=9, default=STATUS["DRAFT"])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def reading_time(self):
        return len(self.content.split()) // READING_SPEED_IN_WORDS_PER_MINUTE

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.title))
            slug = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'articles'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tags'


class ArticleComments(MPTTModel):
    content = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey('Article', related_name='comments', on_delete=models.CASCADE)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        db_table = 'article_comments'


class ArticleLikes(models.Model):
    pk = models.CompositePrimaryKey('article_id', 'user_id')

    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = 'article_likes'

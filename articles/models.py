from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='articles')
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'articles'

class Tag(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'tags'

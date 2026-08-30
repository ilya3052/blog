from django_filters import rest_framework as filters

from articles.models import Article

class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class ArticleFilter(filters.FilterSet):
    ordering = filters.ChoiceFilter(
        choices=[
            ('latest', 'Latest'),
            ('popular', 'Popular'),
            ('likes', 'Likes'),
            ('views', 'Views'),
        ],
        method='filter_ordering',
    )
    tags = CharFilterInFilter(field_name='tags__name', lookup_expr='in')
    class Meta:
        model = Article
        fields = []

    def filter_ordering(self, queryset, name, value):
        ordering = {
            'latest': '-created_at',
            'popular': '-views',
            'likes': '-likes_count',
        }

        return queryset.order_by(ordering.get(value, '-created_at'))

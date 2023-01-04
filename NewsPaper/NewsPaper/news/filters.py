from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category
from django.forms import DateInput


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='post_category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='select category',
    )

    date_creation_after = DateFilter(
        field_name='date_creation',
        label='Date of publication from',
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%dT',
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }

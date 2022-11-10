from django_filters import FilterSet, ModelChoiceFilter, DateFilter, ChoiceFilter
from .models import Post, Category, PostCategory
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


# class CategoryForm(FilterSet):
#     post_category = ChoiceFilter(choices=PostCategory.objects.all())
#
#     class Meta:
#         model = Post
#         fields = ['post_category']

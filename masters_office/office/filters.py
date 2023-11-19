from django_filters import FilterSet, DateRangeFilter, ModelChoiceFilter, BooleanFilter

from .models import Personal, PostWalking, PostRepairWork, PostOrder
from .utils import ResolutionBooleanWidget, filter_district, filter_foreman, filter_author


class PersonalFilter(FilterSet):

    class Meta:
        model = Personal
        fields = {
            'tab_number': ['icontains'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'middle_name': ['icontains'],
            'position': ['exact'],
            'rank': ['exact'],
        }


class PostWalkingFilter(FilterSet):
    date_range = DateRangeFilter(field_name='walk_date')
    author = ModelChoiceFilter(field_name='author', queryset=filter_author)
    resolution = BooleanFilter(
        field_name='resolution',
        lookup_expr='isnull',
        label='С резолюцией',
        widget=ResolutionBooleanWidget
    )

    class Meta:
        model = PostWalking
        fields = [
            'number_post',
            'planned',
            'not_planned',
            'date_range',
            'author',
            'resolution',
            'is_deleted',
        ]


class PostRepairWorkFilter(FilterSet):
    date_range = DateRangeFilter(field_name='date_start_working')
    district = ModelChoiceFilter(field_name='district', queryset=filter_district)
    author = ModelChoiceFilter(field_name='author', queryset=filter_author)

    class Meta:
        model = PostRepairWork
        fields = [
            'number_post',
            'district',
            'order',
            'number_order',
            'date_range',
            'author',
            'is_deleted'
        ]


class PostOrderFilter(FilterSet):
    date_range = DateRangeFilter(field_name='date_start_working')
    district = ModelChoiceFilter(field_name='district', queryset=filter_district)
    foreman = ModelChoiceFilter(field_name='foreman', queryset=filter_foreman)
    author = ModelChoiceFilter(field_name='author', queryset=filter_author)

    class Meta:
        model = PostOrder
        fields = [
            'district',
            'order',
            'number_order',
            'foreman',
            'date_range',
            'author',
            'is_deleted'
        ]

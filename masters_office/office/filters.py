from django_filters import FilterSet, DateRangeFilter, ModelChoiceFilter, BooleanFilter

from .models import Personal, PostWalking, PostRepairWork, PostOrder
from .utils import PostBooleanWidget, filter_district, filter_foreman, filter_author


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
    planned = BooleanFilter(
        field_name='planned',
        lookup_expr='isnull',
        label='Плановый',
        widget=PostBooleanWidget
    )
    not_planned = BooleanFilter(
        field_name='not_planned',
        lookup_expr='isnull',
        label='Внеплановый',
        widget=PostBooleanWidget
    )
    resolution = BooleanFilter(
        field_name='resolution',
        lookup_expr='isnull',
        label='С резолюцией',
        widget=PostBooleanWidget
    )
    is_deleted = BooleanFilter(
        field_name='is_deleted',
        lookup_expr='isnull',
        label='Удаленная запись',
        widget=PostBooleanWidget
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
    is_deleted = BooleanFilter(
        field_name='is_deleted',
        lookup_expr='isnull',
        label='Удаленная запись',
        widget=PostBooleanWidget
    )

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

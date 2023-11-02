from django_filters import FilterSet, DateRangeFilter
from .models import Personal, PostWalking, PostRepairWork


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

    class Meta:
        model = PostWalking
        fields = [
            'number_post',
            'planned',
            'not_planned',
            'date_range',
            'author',
            'is_deleted',
        ]


class PostRepairWorkFilter(FilterSet):
    date_range = DateRangeFilter(field_name='date_start_working')

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

from django_filters import FilterSet
from .models import Personal, PostWalking


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

    class Meta:
        model = PostWalking
        fields = {
            'number_post': ['exact'],
            'planned': ['exact'],
            'not_planned': ['exact'],
            'is_deleted': ['exact'],
        }

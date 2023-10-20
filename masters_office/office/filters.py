from django_filters import FilterSet

from .models import Personal


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

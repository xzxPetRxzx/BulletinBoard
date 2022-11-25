from django_filters import FilterSet
from .models import Reaction


class ReactionFilter(FilterSet):
    class Meta:
        model = Reaction
        fields = {'announce__heading': ['icontains']}

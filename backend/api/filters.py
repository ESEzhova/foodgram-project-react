from django_filters import rest_framework as django_filter
from rest_framework import filters, pagination

from users.models import CustomUser
from recipes.models import Recipe


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'


class RecipeFilter(django_filter.FilterSet):
    author = django_filter.ModelChoiceFilter(
        queryset=CustomUser.objects.all())
    tags = django_filter.AllValuesMultipleFilter(
        field_name='tags__slug')
    is_favorited = django_filter.BooleanFilter(
        method='get_is_favorited')
    is_in_shopping_cart = django_filter.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(carts__user=self.request.user)
        return queryset.all()


class CustomPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'

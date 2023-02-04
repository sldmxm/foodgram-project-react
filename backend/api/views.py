from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPagePagination
from api.permissions import IsAuthorAdminOrReadOnly
from api.serializers import (
    TagSerializer,
    RecipeViewSerializer,
    RecipeEditSerializer,
)
from recipes.models import Tag, Recipe
from users.models import User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeViewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', ]
    pagination_class = LimitPagePagination

    def get_permissions(self):
        if self.action == ('list', 'retrieve', 'create'):
            return [IsAuthenticated(), ]
        return [IsAuthorAdminOrReadOnly(), ]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeEditSerializer
        return RecipeViewSerializer

    def get_queryset(self):
        queryset = (Recipe.objects
                    .select_related('author')
                    .prefetch_related('tags', 'ingredients')
                    )

        author_id = self.request.query_params.get('author')
        if author_id is not None:
            author = get_object_or_404(User, id=author_id)
            queryset = author.recipes.prefetch_related('tags', 'ingredients')

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and int(is_favorited) == 1:
            queryset = self.request.user.favorite_recipes.prefetch_related('tags', 'ingredients')

        is_in_shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            queryset = self.request.user.cart.recipes.prefetch_related('tags', 'ingredients')

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_serializer = RecipeViewSerializer(
            instance=serializer.instance,
            context={'request': request}
        )
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        response_serializer = RecipeViewSerializer(
            instance=serializer.instance,
            context={'request': request}
        )
        return Response(response_serializer.data)

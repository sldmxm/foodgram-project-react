import io

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import (
    viewsets, status, mixins, serializers
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from djoser.views import UserViewSet

from api.pagination import LimitPagePagination
from api.permissions import (
    IsAuthorAdminOrReadOnly,
)
from api.serializers import (
    TagSerializer,
    RecipeViewSerializer,
    RecipeEditSerializer,
    ShortRecipeSerializer,
    SubscriptionsViewSerializer,
    SubscriptionSerializer,
    IngredientSerializer,
)
from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    Cart,
)
from users.models import User, Follow


class UserViewSet(UserViewSet):
    pagination_class = LimitPagePagination
    http_method_names = ['get', 'post', ]
    permission_classes = [AllowAny, ]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        keyword = self.request.query_params.get('name', '')
        queryset = Ingredient.objects.filter(
            Q(name__istartswith=keyword) |
            Q(name__contains=keyword)
        )
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeViewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', ]
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
        queryset = (
            Recipe.objects
            .select_related('author')
            .prefetch_related('tags', 'ingredients')
        )

        author_id = self.request.query_params.get('author')
        if author_id is not None:
            author = get_object_or_404(User, id=author_id)
            queryset = (
                author.recipes
                .prefetch_related('tags', 'ingredients')
            )

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and int(is_favorited) == 1:
            queryset = (
                self.request.user.favorite_recipes
                .prefetch_related('tags', 'ingredients')
            )

        is_in_shopping_cart = (
            self.request.query_params
            .get('is_in_shopping_cart')
        )
        if (is_in_shopping_cart is not None
                and int(is_in_shopping_cart) == 1):
            try:
                queryset = (
                    self.request.user.cart.recipes
                    .prefetch_related('tags', 'ingredients')
                )
            except User.cart.RelatedObjectDoesNotExist:
                queryset = Cart.objects.none()

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
        serializer = (
            self.get_serializer(
                instance,
                data=request.data,
                partial=False
            )
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        response_serializer = RecipeViewSerializer(
            instance=serializer.instance,
            context={'request': request}
        )
        return Response(response_serializer.data)

    def edit_cart_or_favorite(self, request, recipe_id, obj):
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        if request.method == 'POST':
            obj.add(recipe)
            return Response(
                ShortRecipeSerializer(
                    instance=recipe,
                ).data,
                status=status.HTTP_201_CREATED,
            )

        if request.method == 'DELETE':
            obj.remove(recipe)
            return Response(
                {},
                status=status.HTTP_200_OK,
            )
        raise serializers.ValidationError(
            {"errors": "Something went wrong"}
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return self.edit_cart_or_favorite(
            request=request,
            recipe_id=pk,
            obj=cart.recipes,
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return self.edit_cart_or_favorite(
            request=request,
            recipe_id=pk,
            obj=user.favorite_recipes,
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        if self.request.user.is_authenticated:
            return generate_shopping_cart_pdf(self.request.user)
        return Response(
            {
                "detail": "Authentication credentials were not provided."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class SubscriptionsListViewSet(mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SubscriptionsViewSerializer
    pagination_class = LimitPagePagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return (
            User.objects.filter(
                followers__follower=self.request.user
            )
        )


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            Follow,
            follower=self.request.user,
            author_id=self.kwargs['user_id']
        )

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={'author': int(self.kwargs['user_id'])}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_serializer = SubscriptionsViewSerializer(
            instance=serializer.instance.author,
            context={'request': request},
        )
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def generate_pdf(title, ingredient_list, filename):
    MIN_ADDITION_SPACES = 3

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, bottomup=0)
    pdfmetrics.registerFont(TTFont('Russian', 'RobotoMono-Regular.ttf'))

    p.setFont('Russian', 16)
    p.drawString(60, 50, title.encode('utf-8'))
    p.line(60, 55, 530, 55)

    p.setFont('Russian', 12)
    text_object = p.beginText(60, 80)
    max_line_length = 0
    for name, volume in ingredient_list:
        max_line_length = max(
            max_line_length,
            len(f'{name}{volume}') + MIN_ADDITION_SPACES
        )
    for name, volume in ingredient_list:
        additional_spaces = max_line_length - len(f'{name}{volume}')
        text_object.textLine(
            f'{chr(2610)} {name}:{"_" * additional_spaces}{volume}'
            .encode('utf-8')
        )
    p.drawText(text_object)

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)


def generate_ingredient_list(user):
    recipes = user.cart.recipes.all()

    ingredient_list = {}
    for recipe in recipes:
        for ingredient in recipe.ingredients.select_related('ingredient'):
            ingredient_list[str(ingredient.ingredient)] = (
                ingredient_list.get(str(ingredient.ingredient), 0)
                + ingredient.amount)

    return sorted(ingredient_list.items())


def generate_shopping_cart_pdf(user):
    return generate_pdf(
        title=f"{user.first_name}'s shopping cart",
        ingredient_list=generate_ingredient_list(user),
        filename='shopping_cart.pdf'
    )

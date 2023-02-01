from rest_framework import viewsets

from api.serializers import TagSerializer
from recipes.models import Tag


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

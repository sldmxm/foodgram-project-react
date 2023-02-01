from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router = DefaultRouter()


# router.register('categories', views.CategoryViewSet)
# router.register('genres', views.GenresViewSet)
# router.register('titles', views.TitlesViewSet)
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     views.ReviewViewSet, basename='reviews')
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     views.CommentViewSet, basename='comments')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('', include(router.urls)),
]

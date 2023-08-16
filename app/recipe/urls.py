from django.urls import (path, include)
from rest_framework.routers import DefaultRouter

from recipe import views
router = DefaultRouter()
router.register('recipe', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ing', views.IngredidentViewSet)
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/tags/',
         views.RecipeTagsListView.as_view(), name='recipe-tags-list'),
    path('recipe/image/<int:recipe_id>/x',
         views.CreateImageForRecepie.as_view())



]

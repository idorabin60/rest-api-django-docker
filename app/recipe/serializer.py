"""Serializers for recipe API'S"""
from rest_framework import serializers
from core.models import Recipe
from core.models import Tag
from core.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', ]
        read_only_fields = ['id']


class TagSerialzier(serializers.ModelSerializer):
    """serialzier for tags"""
    class Meta:
        model = Tag
        fields = ['id', 'name', ]
        read_only_fields = ['id']


class RecipeDetailSerialzier(serializers.ModelSerializer):
    tags = TagSerialzier(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes',
                  'price', 'link', 'description', 'tags', 'ingredients', 'image']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_data, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            recipe.tags.add(tag_data)

    def _get_or_create_ingredient(self, ingredients, recipe):
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_data, created = Ingredient.objects.get_or_create(user=auth_user,
                                                                        **ingredient)
            recipe.ingredients.add(ingredient_data)

    def create(self, validated_data):
        """Create a recepie"""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredient(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Update Recipe"""
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredient.clear()
            self._get_or_create_ingredient(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RecipeSerializer(serializers.ModelSerializer):
    """Seraizliers for recipes"""
    tags = TagSerialzier(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']

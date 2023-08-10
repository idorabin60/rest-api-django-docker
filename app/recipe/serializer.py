"""Serializers for recipe API'S"""
from rest_framework import serializers
from core.models import Recipe
from core.models import Tag


class TagSerialzier(serializers.ModelSerializer):
    """serialzier for tags"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeDetailSerialzier(serializers.ModelSerializer):
    tags = TagSerialzier(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes',
                  'price', 'link', 'description', 'tags']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Seraizliers for recipes"""
    tags = TagSerialzier(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

"""Serializers for recipe API'S"""
from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Seraizliers for recipes"""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerialzier(RecipeSerializer):
    """Serialzier for recepie details"""
    fields = RecipeSerializer.Meta.fields + ['description']

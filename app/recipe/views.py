from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from core.models import Recipe
from core.models import Tag
from recipe.serializer import RecipeDetailSerialzier, RecipeSerializer, TagSerialzier


class RecipeViewSet(viewsets.ModelViewSet):
    """Mneage recipe APIs"""
    serializer_class = RecipeDetailSerialzier  # Corrected spelling here
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """manage tag in the db"""
    serializer_class = TagSerialzier
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# Create your views here.

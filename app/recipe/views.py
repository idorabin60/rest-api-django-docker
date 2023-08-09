from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Mneage recipe APIs"""
    serializer_class = serializer.RecipeDetailSerialzier  # Corrected spelling here
    queryset = Recipe.objects.all()
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializer.RecipeSerializer
        return self.serializer_class

# Create your views here.

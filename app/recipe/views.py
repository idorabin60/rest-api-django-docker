from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from core.models import Recipe
from core.models import Tag
from core.models import Ingredient
from recipe.serializer import RecipeDetailSerialzier, RecipeSerializer, TagSerialzier, IngredientSerializer, ImageSerializer
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import GenericAPIView


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
        if self.action == 'upload_image':
            return ImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image to recepie"""
        recpie = self.get_object()
        serialzer = self.get_serializer(recpie, data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data)


class TagViewSet(viewsets.ModelViewSet):
    """manage tag in the db"""
    serializer_class = TagSerialzier
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return ImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image to recepie"""
        recpie = self.get_object()
        serialzer = self.get_serializer(recpie, data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data)


class CreateImageForRecepie(GenericAPIView):
    queryset = Recipe.objects.all()  # Modify this queryset as needed
    serializer_class = ImageSerializer

    def post(self, request, pk):
        recepie = Recipe.objects.get(pk=pk)
        serializer = self.get_serializer(recepie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RecipeTagsListView(generics.ListAPIView):
    serializer_class = TagSerialzier

    def get_queryset(self):
        # Assuming you're passing recipe_id in URL
        recipe_id = self.kwargs['recipe_id']
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            return recipe.tags.all()
        except Recipe.DoesNotExist:
            return []


class IngredidentViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


# Create your views here.

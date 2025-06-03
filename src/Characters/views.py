from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Character
from .serializers import CharacterSerializer

# comments to test github action
class CharacterViewSet(viewsets.ViewSet):
    def list(self, request):
        # GET /characters/
        characters = Character.objects.all()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # GET /characters/{pk}/
        character = get_object_or_404(Character, pk=pk)
        serializer = CharacterSerializer(character)
        return Response(serializer.data)

    def create(self, request):
        # POST /characters/
        serializer = CharacterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # DELETE /characters/{pk}/
        character = get_object_or_404(Character, pk=pk)
        character.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

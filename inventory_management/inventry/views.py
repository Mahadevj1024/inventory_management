from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache
import logging
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User 
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
logger = logging.getLogger(__name__)



class ItemCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        item_name = request.data.get('name')
        # Check if the item already exists
        if Item.objects.filter(name=item_name).exists():
            logger.error("Item already exists")
            return Response({"error": "Item already exists"}, status=status.HTTP_409_CONFLICT)
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Invalidate cache after creation
            cache.delete('items')
            logger.info(f"Item created: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Item creation failed")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetail(APIView):
    
    def get(self, request, item_id):
        item = cache.get(f'item_{item_id}')
        if not item:
            try:
                item = Item.objects.get(id=item_id)
                cache.set(f'item_{item_id}', item, timeout=60)
                logger.info(f"Item {item_id} fetched from DB")
            except Item.DoesNotExist:
                logger.error(f"Item {item_id} not found")
                return Response({"error": f"Item {item_id} not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": f"Item {item_id} not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'item_{item_id}')
            logger.info(f"Item {item_id} updated")
            return Response(serializer.data)
        logger.error(f"Failed to update item {item_id}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            cache.delete(f'item_{item_id}')
            logger.info(f"Item {item_id} deleted")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            logger.error(f"Item {item_id} not found")
            return Response({"error": f"Item {item_id} not found"},status=status.HTTP_404_NOT_FOUND)


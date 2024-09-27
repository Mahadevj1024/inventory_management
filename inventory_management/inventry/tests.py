from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item


class ItemTests(APITestCase):

    def test_create_item(self):
        url = reverse('item-create')
        data = {'name': 'Laptop', 'description': 'A personal laptop', 'quantity': 5, 'price': 999.99}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_item(self):
        item = Item.objects.create(name="Mouse", description="Wireless Mouse", quantity=10, price=25.99)
        url = reverse('item-detail', kwargs={'item_id': item.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        item = Item.objects.create(name="Keyboard", description="Mechanical Keyboard", quantity=15, price=49.99)
        url = reverse('item-detail', kwargs={'item_id': item.id})
        data = {'name': 'Keyboard', 'description': 'Updated Description', 'quantity': 10, 'price': 39.99}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        item = Item.objects.create(name="Monitor", description="LED Monitor", quantity=8, price=199.99)
        url = reverse('item-detail', kwargs={'item_id': item.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

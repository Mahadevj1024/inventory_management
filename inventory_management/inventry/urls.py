from django.urls import path
from .views import ItemCreate, ItemDetail



urlpatterns = [
    path('items/', ItemCreate.as_view(), name='item-create'),
    path('items/<int:item_id>/', ItemDetail.as_view(), name='item-detail'),
]

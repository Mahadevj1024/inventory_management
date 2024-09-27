from django.urls import path
from .views import ItemCreate, ItemDetail,LoginView



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'), 
    path('items/', ItemCreate.as_view(), name='item-create'),
    path('items/<int:item_id>/', ItemDetail.as_view(), name='item-detail'),
]

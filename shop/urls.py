from django.urls import path, include
from . import views

urlpatterns = [
    path('item_list/', views.item_list, name='item_list'),
    path('item/<int:pk>/', views.item),
]
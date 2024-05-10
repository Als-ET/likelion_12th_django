from django.urls import path, include
from . import views

urlpatterns = [
    path('item_list/', views.item_list, name='item_list'),
    path('item/<int:pk>/', views.item, name='item'),
    path('item_list_fbv/', views.item_list_fbv, name='item_list_fbv'),
    path('item_list_cbv/', views.ItemListView.as_view(), name='item_list_cbv'),

    path('store_list/', views.store_list, name='store_list'),
    path('store_item_list/<int:store_pk>', views.store_item_list, name='store_item_list'),
    path('search_item/', views.search_item, name='search_item'),

    path('create/', views.create, name='create'),
    path('formcreate/', views.formcreate, name='formcreate'),
    path('modelformcreate/', views.modelformcreate, name='modelformcreate'),
]
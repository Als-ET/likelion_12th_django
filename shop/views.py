from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Item

# 전체 상품 리스트 반환
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        data = []

        for item in items:
            data.append(
                {
                    'id': item.pk,
                    'name': item.name,
                    'store': item.store,
                    'count': item.count,
                    'price': item.price,
                    'image': item.image
                }
            )
        
        return JsonResponse(data)

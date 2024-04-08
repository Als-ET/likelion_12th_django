from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
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
                    'store': item.store.name,
                    'count': item.count,
                    'price': item.price,
                    'image': request.build_absolute_uri(item.image.url)
                }
            )
        
        return JsonResponse(data=data, safe=False)

def item(request, pk):
    if request.method == 'GET':
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404('board does not exist') 
        
        data = {
            'id': item.pk,
            'name': item.name,
            'store': item.store.name,
            'count': item.count,
            'price': item.price,
            'image': request.build_absolute_uri(item.image.url)
        }
        
        return JsonResponse(data=data, safe=False)
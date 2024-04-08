from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from .models import Item, Store
from django.views.decorators.csrf import csrf_exempt

# 전체 상품 리스트 반환
@csrf_exempt
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
    
    if request.method == 'POST':
        item = Item()
        item.name = request.POST['name']
        item.price = request.POST['price']
        item.count = request.POST['count']
        item.image = request.FILES['image']
        store_name = request.POST['store']

        try:
            store = Store.objects.get(name=store_name)
            item.store = store
        except Store.DoesNotExist:
            raise Http404('store does not exist') 
        item.save()

        return JsonResponse({"success":"item has been saved"})

@csrf_exempt
def item(request, pk):
    if request.method == 'GET':
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404('item does not exist') 
        
        data = {
            'id': item.pk,
            'name': item.name,
            'store': item.store.name,
            'count': item.count,
            'price': item.price,
            'image': request.build_absolute_uri(item.image.url)
        }

        return JsonResponse(data=data, safe=False)
    
    if request.method == 'DELETE':
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404('item does not exist')
        
        item.delete()

        return JsonResponse({"success":"item has been deleted"})
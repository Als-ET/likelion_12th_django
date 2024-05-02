from django.http import JsonResponse, Http404
from .models import Item, Store
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.shortcuts import render

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
        
        return JsonResponse(data=data, safe=False, status=200)
    
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

        return JsonResponse({"success":"item has been saved"}, status=201)

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

        return JsonResponse(data=data, safe=False, status=200)
    
    if request.method == 'DELETE':
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404('item does not exist')
        
        item.delete()

        return JsonResponse(data={"success":"item has been deleted"}, status=204)
    


# CBV와 FBV
def item_list_fbv(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'object_list': items})

class ItemListView(ListView):
    model=Item
    template_name='item_list.html'

# 쇼핑몰 기능 구현

# 상점 리스트
def store_list(request):
    stores = Store.objects.all()
    data = []

    for store in stores:
        items = Item.objects.filter(store=store)
        item_count = items.count()
        data.append(
            {
                'id': store.pk,
                'name': store.name,
                'address': store.address,
                'item_count': item_count
            }
        )

    return JsonResponse(data=data, safe=False, status=200)
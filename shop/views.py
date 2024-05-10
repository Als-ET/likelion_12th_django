from django.http import JsonResponse, Http404
from .models import Item, Store
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ItemForm, ItemModelForm

@csrf_exempt
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        
        context = {
            'items': items
        }
        
        return render(request, 'item_list.html', context)
    
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
        
        context = {
            'item': item
        }
        
        return render(request, 'item_detail.html', context)
    
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
    return render(request, 'item_list.html', {'items': items})

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

# 상점별 아이템 리스트
def store_item_list(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)

    sort_criteria = request.GET.get('sorting')

    if sort_criteria == 'update_date':
        items = Item.objects.filter(store=store)
    elif sort_criteria == 'descending-price':
        items = Item.objects.filter(store=store).order_by('-price')
    elif sort_criteria == 'ascending-price':
        items = Item.objects.filter(store=store).order_by('price')
    elif sort_criteria == 'name':
        items = Item.objects.filter(store=store).order_by('name')
    else :
        items = Item.objects.filter(store=store)
    
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

# 아이템 검색
def search_item(request):
    keyword = request.GET.get('keyword')

    items = Item.objects.filter(name__contains=keyword)

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


# html form 을 이용해 쇼핑 아이템(Item) 객체 만들기
def create(request):
    if(request.method == 'POST'):
        item = Item()
        item.name = request.POST['name']
        
        store_name = request.POST['store']
        item.store = get_object_or_404(Store, name=store_name)
        item.count = request.POST['count']
        item.price = request.POST['price']
        item.save()
    return render(request, 'create.html')

# django form을 이용해 쇼핑 아이템(Item) 객체 만들기
def formcreate(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = Item()
            item.name = form.cleaned_data['name']
            item.price = form.cleaned_data['price']
            item.count = form.cleaned_data['count']
            store_name = form.cleaned_data['store']
            item.store = get_object_or_404(Store, name=store_name)
            item.image = form.cleaned_data['image']
            item.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'form_create.html', {'form':form})

# django modelform을 이용해 쇼핑 아이템(Item) 객체 만들기
def modelformcreate(request):
    if request.method == 'POST':
        form = ItemModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemModelForm()
    return render(request, 'form_create.html', {'form':form})

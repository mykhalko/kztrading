from functools import reduce

from django.http import JsonResponse
from django.db.models import Q

from products.models import Product


def add_to_cart(request):
    item_id = request.POST.get('item_id', None)
    if item_id is None:
        return JsonResponse({
            'addition': False,
            'errors': 'no item id'
        })
    item = Product.objects.filter(id=item_id)
    if not item.exists():
        return JsonResponse(
            {'addition': False,
             'errors': 'item not found',
             'id': item_id
             })
    if request.session.get('cart_items'):
        request.session['cart_items'].append(item_id)
    else:
        request.session['cart_items'] = [item_id]
    request.session['cart_items_amount'] = len(request.session.get('cart_items'))
    return JsonResponse({
        'addition': True,
        'id': item_id
    })


def get_cart_items(request):
    items = request.session.get('cart_items')
    if not items:
        return JsonResponse({
            'availability': False
        })
    query = reduce(lambda total, item: total | item, [Q(id=item_id) for item_id in items])
    queryset = Product.objects.filter(query)
    return JsonResponse({
        'availability': True,
        'objects': queryset
    })

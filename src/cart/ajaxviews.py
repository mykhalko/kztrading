from functools import reduce

from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from products.models import Product


@csrf_exempt
def add_to_cart(request):
    id = request.POST.get('id', None)
    print('#id is', id, 'type is', type(id))
    if id is None:
        return JsonResponse({
            'success': False,
            'errors': 'no item id provided'
        })
    item = Product.objects.filter(id=id)
    if not item.exists():
        return JsonResponse(
            {'success': False,
             'errors': 'item not found',
             'id': id
             })
    cart_items = request.session.get('cart_items')
    if cart_items:
        if id in cart_items:
            return JsonResponse({
                'success': False,
                'id': id,
                'errors': 'item already in cart'
            })
        cart_items.append(id)
    else:
        cart_items = [id]
        request.session['cart_items'] = cart_items
    request.session['purchases_amount'] = len(cart_items)
    return JsonResponse({
        'success': True,
        'id': id
    })

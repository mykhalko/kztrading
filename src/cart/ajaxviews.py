from functools import reduce

from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from products.models import Product


@csrf_exempt
def add_to_cart(request):
    id = request.POST.get('id', None)
    if id is None:
        return JsonResponse({
            'success': False,
            'errors': 'no item id provided'
        })
    id = int(id)
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


class RemoveView(View):

    http_method_names = ['post']

    def __init__(self, *args, **kwargs):
        self.request = None
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.request = request
        item = request.POST.get('item', None)
        if item and item in request.session.get('cart_items'):
            request.session['cart_items'].remove(item)
            purchases_amount = request.session['purchases_amount']
            request.session['purchases_amount'] = purchases_amount - 1
        else:
            request.session['cart_items'] = None
            request.session['purchases_amount'] = 0
        return JsonResponse({
            'success': True
        })

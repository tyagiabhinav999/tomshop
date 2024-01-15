from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product, Collection, Order, OrderItem

# Create your views here.
def say_hello(request):
    # collections = Collection.objects.filter(featured_product__isnull = True)
    orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # order_items = OrderItem.objects.select_related('order__customer')[:5] # .filter(inventory__lt = 20).filter(unit_price__lt = 20)
    return render(request, 'hello.html', {'name': 'Abhinav', 'orders': list(orders)})


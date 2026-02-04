from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from apps.products.models import Product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.select_related('product').filter(cart=cart)
    total = sum([item.product.narxi * item.number for item in items])
    return render(request, 'carts/cart_detail.html', {
        'items': items,
        'total': total,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.number+=1
        item.save()
    return redirect('cart_detail')

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
        if quantity <= 0:
            item.delete()
        else:
            item.number = quantity
            item.save()
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')

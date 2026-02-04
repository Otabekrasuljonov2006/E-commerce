from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from apps.carts.models import Cart, CartItem
from .models import Order, OrderItem
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User
from django.http import HttpResponse

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.select_related('product').filter(cart=cart)

    if not cart_items.exists():
        return redirect('product_list')

    for item in cart_items:
        if item.product.omborda_bor < item.number:
            return redirect('cart_detail')

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total_price=0,
            status='pending'
        )

        total = 0

        for item in cart_items:
            price = item.product.narxi
            quantity = item.number

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=quantity,
                price_at_time=price
            )

            item.product.omborda_bor -= quantity
            item.product.save()

            total += price * quantity

        order.total_price = total
        order.save()

        cart_items.delete()

    return redirect('product_list')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {
        'orders': orders
    })
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': order_items
    })
@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'pending':
        order.status = 'paid'
        order.save()

    return redirect('order_detail', order_id=order.id)


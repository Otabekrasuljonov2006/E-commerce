from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
def product_list(request):
    products = Product.objects.select_related('category').order_by('-qoshgan_sana')
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    })
def product_detail(request, pk):
    product=get_object_or_404(Product, pk = pk)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })

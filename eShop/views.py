from django.shortcuts import render
from product_store.models import Product


def home(request):
    products = Product.objects.all().filter(status=True)[:8]

    context = {
        'products': products
    }

    return render(request, 'home.html', context)

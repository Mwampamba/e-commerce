from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from product_catalog.models import Category
from product_order.models import ProductOrder
from .models import Product, Rating


def product_store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.filter(
            product_category=categories, status=True)
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        total_products = products.count()

    else:
        products = Product.objects.all().filter(status=True).order_by('id')
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        total_products = products.count()

    context = {
        'products': paged_products,
        'total_products': total_products
    }

    return render(request, 'product/store.html', context)


def product_detail(request, category_slug, product_slug):
    categories = None
    try:
        if category_slug != None:
            categories = get_object_or_404(Category, category_slug=category_slug)
            product = Product.objects.get(
                product_category__category_slug=category_slug, product_slug=product_slug)
        
        related_products = Product.objects.filter(
            product_category=categories, status=True).order_by('id')[1:]

    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = ProductOrder.objects.filter(
                user=request.user, product_id=product.id).exists()

        except ProductOrder.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = Rating.objects.filter(product_id=product.id, status=True).order_by('-created_at')
    reviews_count = reviews.count()

    context = {
        'product': product,
        'related_products': related_products,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'reviews_count': reviews_count
    }

    return render(request, 'product/details.html', context)


def search_product(request):
    if 'q' in request.GET:
        keyword = request.GET['q']
        if keyword:
            products = Product.objects.order_by('id').filter(
                Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            total_products = products.count()

    context = {
        'products': paged_products,
        'total_products': total_products,
    }

    return render(request, 'product/store.html', context)


class RatingAndReview(View):
    def get(self, request):
        return render(request, 'product/details.html')

    def post(self, request, product_id):
        current_url = request.META.get('HTTP_REFERER')
        subject = request.POST.get('subject', False)
        review = request.POST.get('review', False)
        rate = request.POST.get('rating', False)
        product_id = product_id
        user_id = request.user.id

        Rating.objects.create(
            subject=subject, review=review, rate=rate, product_id=product_id, user_id=user_id, status=True)

        messages.success(request, 'Thank you! your review has been submited.')

        return redirect(current_url)


@login_required(login_url = 'login')
def similar_product_suggestion(request):
    # Get the customer's purchase history
    customer_orders = ProductOrder.objects.filter(user=request.user)
    # Get a list of product IDs that the customer has purchased before
    purchased_product_ids = customer_orders.values_list('product__id', flat=True)
    # Get a list of other customers who have purchased the same products as the current customer
    similar_customers = ProductOrder.objects.filter(product__in=purchased_product_ids) \
                        .exclude(user=request.user) \
                        .values('user') \
                        .annotate(num_products=Count('product')) 

    # Get a list of recommended products based on the purchase history of similar customers
    recommended_products = ProductOrder.objects.filter(order__user__in=[customer['user'] for customer in similar_customers]) \
                          .exclude(id__in=purchased_product_ids)[:6]

    context = {
        'recommended_products': recommended_products
    }
    
    return render(request, 'product/store.html', context)


from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Product


def product_list(request):
    products = Product.objects.all()

    # Filters
    product_type = request.GET.get("type")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    category = request.GET.get("category")
    brand = request.GET.get("brand")
    availability = request.GET.get("availability")
    search = request.GET.get("search")

    if product_type:
        products = products.filter(type__icontains=product_type)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if category:
        products = products.filter(category__icontains=category)

    if brand:
        products = products.filter(brand__icontains=brand)

    if availability:
        products = products.filter(stock__gte=1 if availability == "in_stock" else 0)

    if search:
        products = products.filter(name__icontains=search)

    # Pagination
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, deliver the first page.
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # If page_number is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.get_page(paginator.num_pages)
    print(page_obj)
    return render(
        request,
        "store/product_list.html",
        {
            "page_obj": page_obj,
            "product_type": product_type,
            "min_price": min_price,
            "max_price": max_price,
            "category": category,
            "brand": brand,
            "availability": availability,
            "search": search,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "store/product_detail.html", {"product": product})

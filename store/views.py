from decimal import Decimal
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Order, OrderItem, Product


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


# Add to Cart
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get("cart", {})
    print(cart)
    if str(product.id) not in cart:
        cart[str(product.id)] = {"quantity": 1, "price": str(product.price)}
    else:
        cart[str(product.id)]["quantity"] += 1
    print(cart)
    request.session["cart"] = cart
    return redirect("cart")


# View Cart
def view_cart(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = Decimal(0)

    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = Decimal(item["price"]) * item["quantity"]
        cart_items.append(
            {"product": product, "quantity": item["quantity"], "total": item_total}
        )
        total_price += item_total

    return render(
        request,
        "store/cart.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


# Remove from Cart
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session["cart"] = cart
    return redirect("cart")


# Checkout
def checkout(request):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        total_price = Decimal(0)

        # Create order
        order = Order.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            phone_number=request.POST["phone_number"],
            shipping_address=request.POST["shipping_address"],
            total_price=total_price,
        )

        # Add order items
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            item_total = Decimal(item["price"]) * item["quantity"]
            total_price += item_total
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=item["price"],
            )

        # Update order total price
        order.total_price = total_price
        order.save()
        request.session["order_access_key"] = order.access_key
        # Clear the cart
        request.session["cart"] = {}
        print(order.id)
        return redirect("order_detail", orderId=order.id)

    return render(request, "store/checkout.html")


# Order Details
def order_detail(request, orderId):
    print(orderId)
    # Retrieve the access key from the session
    session_access_key = request.session.get("order_access_key")

    # Retrieve the order using  id
    order = get_object_or_404(Order, id=orderId, access_key=session_access_key)
    print(order)
    # Render the order details
    return render(request, "store/order_detail.html", {"order": order})

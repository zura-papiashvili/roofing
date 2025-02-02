from decimal import Decimal
import json
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Order, OrderItem, Product

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


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


def checkout(request):
    cart = request.session.get("cart", {})
    total_price = Decimal(0)
    cart_items = []

    # Calculate the total price for the cart and prepare cart details
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = Decimal(item["price"]) * item["quantity"]
            total_price += item_total
            cart_items.append(
                {
                    "product": product,
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "item_total": item_total,
                }
            )
        except Product.DoesNotExist:
            continue  # Skip any products that don't exist

    total_price_cents = int(total_price * 100)  # Convert to cents

    if request.method == "POST":
        # Create the order
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
            try:
                product = Product.objects.get(id=product_id)
                item_total = Decimal(item["price"]) * item["quantity"]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"],
                    price=item["price"],
                )
            except Product.DoesNotExist:
                continue  # Skip any products that don't exist

        # Update order total price in case of any adjustments
        order.total_price = total_price
        order.save()

        # Store order access key in the session
        request.session["order_access_key"] = order.access_key

        # Clear the cart
        request.session["cart"] = {}

        # Redirect to the order detail page
        return redirect("order_detail", orderId=order.id)

    # Render the checkout page with the total price and order details
    return render(
        request,
        "store/checkout.html",
        {
            "total_price": total_price_cents,
            "cart_items": cart_items,
            "total_price_display": total_price,
        },
    )


@csrf_exempt
def create_payment_intent(request):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = data.get("amount")

        if not amount:
            return JsonResponse({"error": "Amount is required."}, status=400)

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
            )
            return JsonResponse({"clientSecret": payment_intent.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

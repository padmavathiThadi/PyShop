from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from .models import Product, Order, OrderItem, Offer


def index(request):
    products = Product.objects.all()

    search = request.GET.get('search', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    if search:
        products = products.filter(name__icontains=search)

    if min_price:
        try:
            products = products.filter(
                price__gte=Decimal(min_price)
            )
        except (ValueError, TypeError):
            pass

    if max_price:
        try:
            products = products.filter(
                price__lte=Decimal(max_price)
            )
        except (ValueError, TypeError):
            pass

    cart = request.session.get('cart', {})

    return render(request, 'index.html', {
        'products': products,
        'cart_count': sum(cart.values()),
        'search': search,
        'min_price': min_price,
        'max_price': max_price,
    })


def new(request):
    return HttpResponse("New products")


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {str(item): 1 for item in cart}

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('index')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})

    product_ids = [
        int(product_id)
        for product_id in cart.keys()
    ]

    products = Product.objects.filter(
        id__in=product_ids
    )

    cart_products = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        item_total = product.price * quantity

        cart_products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

        total += item_total

    return render(request, 'cart.html', {
        'cart_products': cart_products,
        'cart_count': sum(cart.values()),
        'total': total
    })


def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    product_ids = [
        int(product_id)
        for product_id in cart.keys()
    ]

    products = Product.objects.filter(
        id__in=product_ids
    )

    cart_products = []
    subtotal = 0

    for product in products:
        quantity = cart[str(product.id)]
        item_total = product.price * quantity

        cart_products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

        subtotal += item_total

    discount = None
    discount_amount = Decimal('0')
    discount_percent = 0
    total = subtotal
    discount_error = None

    if request.method == 'POST':

        discount_code = request.POST.get(
            'discount_code',
            ''
        ).strip()

        if discount_code:

            try:
                discount = Offer.objects.get(
                    code__iexact=discount_code
                )

                discount_amount = (
                    subtotal *
                    Decimal(str(discount.discount))
                )

                total = subtotal - discount_amount

                discount_percent = int(
                    discount.discount * 100
                )

                request.session['discount_code'] = (
                    discount.code
                )

                request.session['discount_amount'] = float(
                    discount_amount
                )

                request.session['discount_error'] = False

            except Offer.DoesNotExist:

                discount_error = (
                    'Invalid discount code. '
                    'Please try again.'
                )

                request.session.pop(
                    'discount_code',
                    None
                )

                request.session.pop(
                    'discount_amount',
                    None
                )

                request.session['discount_error'] = True

    else:

        discount_code = request.session.get(
            'discount_code'
        )

        if discount_code:

            try:
                discount = Offer.objects.get(
                    code__iexact=discount_code
                )

                discount_amount = (
                    subtotal *
                    Decimal(str(discount.discount))
                )

                total = subtotal - discount_amount

                discount_percent = int(
                    discount.discount * 100
                )

            except Offer.DoesNotExist:

                request.session.pop(
                    'discount_code',
                    None
                )

                request.session.pop(
                    'discount_amount',
                    None
                )

    return render(request, 'checkout.html', {
        'cart_products': cart_products,
        'cart_count': sum(cart.values()),
        'subtotal': subtotal,
        'discount': discount,
        'discount_amount': discount_amount,
        'discount_percent': discount_percent,
        'discount_error': discount_error,
        'total': total
    })


def place_order(request):

    if request.method != 'POST':
        return redirect('checkout')

    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    # Don't allow checkout if the last discount attempt
    # was invalid.
    if request.session.get('discount_error'):
        return redirect('checkout')

    product_ids = [
        int(product_id)
        for product_id in cart.keys()
    ]

    products = Product.objects.filter(
        id__in=product_ids
    )

    # Check stock
    for product in products:

        quantity = cart[str(product.id)]

        if quantity > product.stock:

            return render(
                request,
                'stock_error.html',
                {
                    'product': product,
                    'requested_quantity': quantity,
                    'available_stock': product.stock
                }
            )

    # Calculate subtotal
    subtotal = 0

    for product in products:

        quantity = cart[str(product.id)]

        subtotal += product.price * quantity

    # Calculate discount
    discount_amount = Decimal('0')

    discount_code = request.session.get(
        'discount_code'
    )

    if discount_code:

        try:

            discount = Offer.objects.get(
                code__iexact=discount_code
            )

            discount_amount = (
                subtotal *
                Decimal(str(discount.discount))
            )

        except Offer.DoesNotExist:

            discount_amount = Decimal('0')

    total = subtotal - discount_amount

    with transaction.atomic():

        order = Order.objects.create(
            customer=request.user,
            total=total
        )

        for product in products:

            quantity = cart[str(product.id)]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            product.stock -= quantity
            product.save()

    # Clear cart and discount
    request.session['cart'] = {}

    request.session.pop(
        'discount_code',
        None
    )

    request.session.pop(
        'discount_amount',
        None
    )

    request.session.pop(
        'discount_error',
        None
    )

    return render(
        request,
        'order_confirmation.html',
        {
            'order': order
        }
    )


def my_orders(request):

    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(
        customer=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_orders.html',
        {
            'orders': orders
        }
    )

def order_detail(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    items = order.items.all()

    for item in items:
        item.item_total = item.price * item.quantity

    return render(request, 'order_detail.html', {
        'order': order,
        'items': items
    })
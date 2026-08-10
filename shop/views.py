from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Order, OrderItem

def home(request):
    products = Product.objects.all()
    q = request.GET.get("q","").strip()
    category = request.GET.get("category","")
    if q:
        products = products.filter(name__icontains=q)
    if category:
        products = products.filter(category=category)
    return render(request, "shop/home.html", {
        "products": products,
        "categories": Product.CATEGORY_CHOICES,
        "q": q, "selected_category": category
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "shop/product_detail.html", {"product": product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect("home")
    cart = request.session.get("cart", {})
    key = str(product_id)
    cart[key] = min(cart.get(key, 0) + 1, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.META.get("HTTP_REFERER", "home"))

def cart(request):
    cart_data = request.session.get("cart", {})
    items, total = [], Decimal("0.00")
    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=int(product_id))
        quantity = min(quantity, product.stock)
        subtotal = product.price * quantity
        items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
        total += subtotal
    return render(request, "shop/cart.html", {"items": items, "total": total})

def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart = request.session.get("cart", {})
    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = min(quantity, product.stock)
    request.session["cart"] = cart
    return redirect("cart")

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")

@login_required
def checkout(request):
    cart_data = request.session.get("cart", {})
    if not cart_data:
        messages.info(request, "Your cart is empty.")
        return redirect("home")
    items, total = [], Decimal("0.00")
    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=int(product_id))
        if quantity > product.stock:
            messages.error(request, f"Only {product.stock} units of {product.name} are available.")
            return redirect("cart")
        subtotal = product.price * quantity
        total += subtotal
        items.append((product, quantity))
    if request.method == "POST":
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                full_name=request.POST.get("full_name",""),
                email=request.POST.get("email",request.user.email),
                address=request.POST.get("address",""),
                city=request.POST.get("city",""),
                postal_code=request.POST.get("postal_code",""),
                total=total,
            )
            for product, quantity in items:
                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
                product.stock -= quantity
                product.save(update_fields=["stock"])
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect("orders")
    return render(request, "shop/checkout.html", {"items": items, "total": total})

@login_required
def orders(request):
    return render(request, "shop/orders.html", {"orders": request.user.orders.prefetch_related("items__product")})

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username","").strip()
        email = request.POST.get("email","").strip()
        password = request.POST.get("password","")
        confirm = request.POST.get("confirm_password","")
        if not username or not email or not password:
            messages.error(request, "Please fill all fields.")
        elif password != confirm:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "Welcome to NEXORA!")
            return redirect("home")
    return render(request, "registration/register.html")

def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect(request.GET.get("next","home"))
        messages.error(request, "Invalid username or password.")
    return render(request, "registration/login.html")

def user_logout(request):
    logout(request)
    return redirect("home")

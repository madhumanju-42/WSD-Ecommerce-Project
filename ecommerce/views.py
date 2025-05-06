from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Product, CartItem, Order, OrderItem, User


def home(request):
    products = Product.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()
    return render(request, 'home.html', {'products': products, 'categories': categories})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error' : 'Invalid Credentials'})
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not user :
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            login(request, user)            
            return redirect('home')
        else:
            return render(request, 'signup.html', {'error': 'Not a Valid User'})
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cartTotal = 0
    for item in cart_items:
        item.total = item.quantity * item.product.price 
        cartTotal += item.total
    cart_items.cartTotal = cartTotal
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    cart_item.quantity += int(request.POST.get('quantity', 0))
    cart_item.save()
    return redirect('home')

@login_required
def remove_from_cart(request, product_id):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items.exists():
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        cart_items.delete()
    return redirect('thankyou')

@login_required
def thank_you(request):
    return render(request, 'thankyou.html')

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-timestamp')
    for order in orders:
        order.total = 0 
        order_items = OrderItem.objects.filter(order=order)
        
        for item in order_items:
            item.total = item.quantity * item.product.price  
            order.total += item.total
    print(orders[0].orderitem_set.all)
    return render(request, 'orders.html', {'orders': orders})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

def cart_count_api(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
        totalCartItems = 0
        for i in items:
            totalCartItems += i.quantity

        return JsonResponse({'count': totalCartItems})
    return JsonResponse({'count': 0})
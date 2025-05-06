from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('thankyou/', views.thank_you, name='thankyou'),
    path('orders/', views.orders_view, name='orders'),
    path('profile/', views.profile_view, name='profile'),
    path('api/cart-count/', views.cart_count_api, name='cart_count_api'),
    path('signup/', views.signup_view, name='signup')
]
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from . import views



app_name = "shop"

urlpatterns = [
    path('getAccessToken', views.getAccessToken, name='getAccessToken'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Implement custom view for password change and password change done
    #path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    #path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path("home", views.home, name="home"),
    path("affiliate", views.affiliate, name="affiliate"),
    path("products/", views.products, name="products"),
    path("products/<int:category_id>/", views.products, name="products"),
    path("category/<int:category_id>/", views.category, name="category"),
    path("profile", views.profile, name="profile"),
    path("product/<int:product_id>/", views.product, name="product"),
    path("product/<int:product_id>/add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("product/<int:product_id>/remove_from_cart/", views.remove_from_cart, name="remove_from_cart"),
    path('cart/', views.cart, name='cart'),
    path('cart/remove/<int:product_id>/', views.remove, name='remove'),
    path('add_quantity/<int:product_id>/', views.add_quantity, name='add_quantity'),
    path('subtract_quantity/<int:product_id>/', views.subtract_quantity, name='subtract_quantity'),
    path('checkout/', views.checkout, name="checkout"),
    path('stk_callback/', views.process_stk_callback, name="mpesa_callback"),
    path('stk_push/', views.initiate_stk_push, name="stk_push"),
    path('checkout/place_order/<int:cart_id>/', views.place_order, name='place_order'),
    path('stk_push_callback/', views.stk_push_callback, name="stk_push_callback"),
    path('test/', views.test, name='test'),
    path('checkout/order_confirmation/', views.order_confirmation, name='order_confirmation')
]

# Serving media files only during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
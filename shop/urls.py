from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from . import views


app_name = "shop"
urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('signup/', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path("home", TemplateView.as_view(template_name="home.html"),  name="home"),
    path("products", views.products, name="products"),
    path("top_categories", views.top_categories, name="top_categories"),
    path("categories", views.categories, name="categories"),
    path("product/<int:product_id>/", views.product, name="product"),
    path("product/<int:product_id>/add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/<int:cart_id/', views.checkout, name="checkout"),
]
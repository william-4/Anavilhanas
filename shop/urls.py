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
    path("products", views.products, name="products"),
    path("profile", views.profile, name="profile"),
    path("create_product", views.create_product, name="create_product"),
    path("create_category", views.create_category, name="create_category"),
    path("top_categories", views.top_categories, name="top_categories"),
    path("categories", views.categories, name="categories"),
    path("product/<int:product_id>/", views.product, name="product"),
    path("product/<int:product_id>/add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name="checkout"),
]

# Serving media files only during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
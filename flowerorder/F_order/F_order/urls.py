"""
URL configuration for F_order project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf .urls.static import static
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path ('master/', views.Master,name='master'),
    path ('', views.Index,name='index'),    
    path ('about/', views.About,name='about'),
    path('subproduct/<int:id>/', views.subproduct_view, name='subproduct'),  # To show subproducts for a specific product
    path('subproduct2/<int:id>/', views.mainsubproduct_view, name='mainsubproduct'),
    path('subproduct3/<int:id>/', views.lastsubproduct_view, name='sublastproduct'),  # To show subproducts for a specific product

    path ('signup', views.signup,name='signup'),
    path ('accounts/',include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('cart/add/<int:id>/<str:type>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('checkout/',views.CheckOut,name='chackout'),
    path('order/',views.Your_Order,name='order'),

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT )

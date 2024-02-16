"""
URL configuration for ecomm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from ecommapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomeView.as_view(),name='home_view'),
    path('user/reg',views.UserRegView.as_view(),name='reg_view'),
    path('user/log',views.UserLoginView.as_view(),name='log_view'),
    path('user/logout',views.UserLogoutView.as_view(),name='logout_view'),
    path('user/detail<int:id>',views.ProductDetailsView.as_view(),name='detail_view'),
    path('addcart/<int:id>',views.Addtocart.as_view(),name='addcart_1'),
    path('showcart',views.Cartproduct.as_view(),name='crtpr'),
    path('place/order/<int:cart_id>',views.PlaceOrderView.as_view(),name='placeorder_view'),
    path('place/delete/<int:id>',views.CartDeleteView.as_view(),name='cartdelete_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('authentication/', include('users.urls')),
    path('store/', include('product_store.urls')),
    path('cart/', include('product_cart.urls')),
    path('order/', include('product_order.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


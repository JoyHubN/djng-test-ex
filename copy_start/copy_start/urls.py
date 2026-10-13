"""
URL configuration for copy_start project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from tovar.views import (
    home_view, 
    tovar_detail_view, 
    korzina_view, 
    add_to_cart_view, 
    increase_cart_item_view, 
    decrease_cart_item_view, 
    remove_from_cart_view,
    checkout_order_view,
    delete_order_view
)
from about.views import about_view
from where_find_us.views import where_find_us_view
from catalog.views import catalog_view
from users.views import register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('where-find-us/', where_find_us_view, name='where_find_us'),
    path('catalog/', catalog_view, name='catalog'),
    path('tovar/<int:pk>/', tovar_detail_view, name='tovar_detail'),
    path('korzina/', korzina_view, name='korzina'),
    path('korzina/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('korzina/increase/<int:item_id>/', increase_cart_item_view, name='increase_cart_item'),
    path('korzina/decrease/<int:item_id>/', decrease_cart_item_view, name='decrease_cart_item'),
    path('korzina/remove/<int:item_id>/', remove_from_cart_view, name='remove_from_cart'),
    path('korzina/checkout/', checkout_order_view, name='checkout_order'),
    path('korzina/order/delete/<int:order_id>/', delete_order_view, name='delete_order'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

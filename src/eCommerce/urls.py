import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import (about_page, contact_page, index, login_page, logout_page,
                    register_page)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('', index, name='index'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('admin/', admin.site.urls),
    path('products/', include('apps.products.urls')),
    path('search/', include('apps.search.urls')),
    path('cart/', include('apps.cart.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

from django.urls import path

from .views import (FeaturedDetailView, FeaturedListView, ProductDetailView,
                    ProductListView)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(),
         name='list'),

    path('featured/', FeaturedListView.as_view(),
         name='FeaturedList'),

    path('featured/<slug:slug>/', FeaturedDetailView.as_view(),
         name='FeaturedDetail'),

    path('<slug:slug>/', ProductDetailView.as_view(),
         name='detail'),
]

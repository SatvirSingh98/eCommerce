from django.urls import path

from .views import (ProductListView, ProductDetailView,
                    ProductFeaturedListView, ProductFeaturedDetailView)


app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(),
         name='list'),

    path('<int:pk>/', ProductDetailView.as_view(),
         name='detail'),

    path('featured/', ProductFeaturedListView.as_view(),
         name='FeaturedList'),

    path('featured/<int:pk>/', ProductFeaturedDetailView.as_view(),
         name='FeaturedDetail')
]

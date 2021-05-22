from django.views.generic import ListView
from apps.products.models import Product


class ProductSearchView(ListView):
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query is not None:
            return Product.objects.search(query)
        return Product.objects.none()

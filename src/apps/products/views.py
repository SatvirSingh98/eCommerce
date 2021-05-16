# from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Product


class ProductListView(ListView):
    template_name = 'products/product_list.html'
    model = Product  # or queryset = Product.objects.all()
    # or
    # def get_queryset(self):
    #     """
    #     Return the list of product items
    #     """
    #     return Product.objects.all()

    # https://stackoverflow.com/questions/19707237/use-get-queryset-method-or-set-queryset-variable

    # Just to print the context of this class
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     return context


class ProductDetailView(DetailView):
    # model = Product ;not needed anymore because get_object
    # will return the query.
    template_name = 'products/product_detail.html'

    # lookup by slug
    def get_object(self):
        slug = self.kwargs.get('slug')
        # try:
        #     instance = Product.objects.get(slug=slug, active=True)
        # except Product.DoesNotExist:
        #     raise Http404('Not Found...')
        # except Exception:
        #     raise Http404('Huh??')
        # return instance
        # or
        return get_object_or_404(Product, slug=slug, active=True)

    # lookup by id
    # def get_object(self):
    #     instance = Product.objects.get_by_id(self.kwargs.get('pk'))
    #     if instance is None:
    #         raise Http404('No match found')
    #     return instance

    # Just to print the context of this class
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     return context

    # or
    # def get_queryset(self):
    #     return Product.objects.filter(pk=self.kwargs.get('pk'))

# or
# def product_detail_view(request, pk):
    # instance = get_object_or_404(Product, pk=pk)
    # or
    # try:
    #     instance = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     print('No match found')
    #     raise Http404('No match found')
    # except Exception:
    #     print('huh?')
    # or
    # qs = Product.objects.filter(pk=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404('No match found')

    # objects is default model manager and we can also make
    # custom model managers to make more efficient queries.

    # or
    # instance = Product.objects.get_by_id(pk)
    # if instance is None:
    #     raise Http404('No match found')

    # context = {'product': instance}
    # return render(request, 'products/product_detail.html', context)


class FeaturedListView(ListView):
    queryset = Product.objects.all().featured()
    template_name = 'products/product_list.html'


class FeaturedDetailView(DetailView):
    template_name = 'products/product_detail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Product, slug=slug, active=True, featured=True)
        return obj

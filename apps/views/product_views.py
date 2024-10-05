from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from apps.forms import OrderModelForm
from apps.models import Category, Product, Stream


class AllProductListView(ListView):
    queryset = Product.objects.select_related('category').order_by('-created_at')
    template_name = 'apps/index.html'
    context_object_name = 'products'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.GET.get('cat')
        if category:
            return qs.filter(category__slug=category)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductStreamDetail(DetailView, FormView):
    template_name = 'apps/product/product_detail.html'
    form_class = OrderModelForm
    success_url = reverse_lazy('order-detail')

    def get_queryset(self):
        if self.kwargs.get('slug'):
            return Product.objects.all()
        elif self.kwargs.get('pk'):
            return Stream.objects.all()
        return super().get_queryset()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if isinstance(obj, Stream):
            obj.visit_count += 1
            obj.save()
        return obj

    def form_valid(self, form):
        order = form.save()
        return redirect('order-detail', pk=order.id)

    def form_invalid(self, form):
        message = "Invalid phone number!"
        messages.add_message(self.request, messages.WARNING, message)
        product_slug = form.cleaned_data.get('product').slug
        return redirect('product-detail', slug=product_slug)


class ProductSearchListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/search_results.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            return qs.filter(name__icontains=search)
        return qs


class ProductStatisticListView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_statistic.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        session_product = Stream.objects.filter(product_id=self.kwargs.get('pk'), owner=self.request.user)
        ctx['my_stream_count'] = session_product.count()
        return ctx
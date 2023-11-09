from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .filters import ProductFilter
from .pagination import DefaultPagination
from .serializers import ProductsSerializer, CollectionSerializer, ReviewSerializer, CartSerializer
from .models import Product, Collection, OrderItem, Review, Cart


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serializer_class = ProductsSerializer
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk'].count()) > 0:
            return Response({'error': 'Product cannot be deleted'})
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    """
        # http_method_names = ['post', 'get']

        # def destroy(self, request, *args, **kwargs):
        #     if Collection.objects.filter(featured_product=kwargs['pk']).count() > 0:
        #         return Response({'error': 'Collection cannot be deleted because it includes one or more products.'})
        #     return super().destroy(request, *args, **kwargs)
    """


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])


class CartViewSet(CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .filters import ProductFilter
from .serializers import ProductsSerializer, CollectionSerializer, ReviewSerializer
from store.models import Product, Collection, OrderItem, Review


class ProductViewSet(ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

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

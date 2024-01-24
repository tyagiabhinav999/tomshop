from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection, OrderItem
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({"error":"Product can't be deleted."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        queryset = get_object_or_404(Collection.objects.annotate(products_count=Count('product')).all(), pk=pk)
        if queryset.products_count > 0:
            return Response({"error":"Collection can't be deleted."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


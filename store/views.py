from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response({"error":"Product can't be deleted."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)


@api_view()
def collection_list(request):
    collection = Collection.objects.all()
    serializer = CollectionSerializer(collection, many=True)
    return Response(serializer.data)
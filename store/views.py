from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
# Django Rest Framework
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection, Cart
from .serializers import ProductSerializer, CollectionSerializer, CartSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
     
    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
     
    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted'}, status=status.HTTP_204_NO_CONTENT)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


##### WHEN USING ListCreateAPIView
# class ProductList(ListCreateAPIView):
#    queryset = Product.objects.all()
#    serializer_class = ProductSerializer
#    def get_serializer_context(self):
#        return {'request': self.request}
    # When you have some logic
    # def get_queryset(self):
    #    return Product.objects.select_related('collection').all()
    # def get_serializer_class(self):
    #    return ProductSerializer
    ##### WHEN USING APIView
    #def get(self, request):
    #    queryset = Product.objects.select_related('collection').all()
    #    serializer = ProductSerializer(queryset, many=True, context={'request': request})
    #    return Response(serializer.data)   
    #def post(self, request):
    #    serializer = ProductSerializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save()
    #    return Response(serializer.data, status=status.HTTP_201_CREATED)
###### WHEN USING RetrieveUpdateDestroyAPIView
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#    queryset = Product.objects.all()
#    serializer_class = ProductSerializer
#    def delete(self, request, pk):
#        product = get_object_or_404(Product, pk=pk)
#        if product.orderitems.count() > 0:
#            return Response(
#                {'error': 'Product cannot be deleted because it is associated with an order item.'},
#                status=status.HTTP_405_METHOD_NOT_ALLOWED)
#        product.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get(self, request, id):
    #    product = get_object_or_404(Product, pk=id)
    #    serializer = ProductSerializer(product)
    #    return Response(serializer.data)
    # def put(self, request, id):
    #    product = get_object_or_404(Product, pk=id)
    #    serializer = ProductSerializer(product, data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save()
    #    return Response(serializer.data)

#class CollectionList(ListCreateAPIView):
#    queryset = Collection.objects.annotate(products_count=Count('products')).all()
#    serializer_class = CollectionSerializer
#    def get_serializer_context(self):
#        return {'request': self.request}
    #  WHEN USING APIView
    #  def get(self, request):
    #    queryset = Collection.objects.annotate(
    #        products_count=Count('products')).all()
    #    serializer = CollectionSerializer(queryset, many=True, context={'request': request})
    #    return Response(serializer.data) 
    # def post(self, request):
    #    serializer = CollectionSerializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save()
    #    return Response(serializer.data, status=status.HTTP_201_CREATED)       

#class CategoryDetail(RetrieveUpdateDestroyAPIView):
#    queryset = Collection.objects.annotate(products_count=Count('products'))
#    serializer_class = CollectionSerializer

#    def delete(self, request, pk):
#        collection = get_object_or_404(Collection, pk=pk)
#        if collection.products.count() > 0:
#            return Response({'error': 'Collection cannot be deleted'}, status=status.HTTP_204_NO_CONTENT)
#        collection.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
        
    # WHEN USING APIView
    #  collection = get_object_or_404(collection.objects.annotate(products_count=Count('products')), pk=pk)
    # if request.method == 'GET':
    #    serializer = CollectionSerializer(collection)
    #    return Response(serializer.data)
    # elif request.method == 'PUT':
    #    serializer = CollectionSerializer(collection, data=request)
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save()
    #    return Response(serializer.data)
    # elif request.method == 'DELETE':
    #    if collection.products.count() > 0:
    #        return Response(
    #            {'error': 'Collection cannot be deleted'},
    #            status=status.HTTP_204_NO_CONTENT)
    #         collection.delete()
    #    return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
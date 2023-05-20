from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
# Django Rest Framework
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .models import Product, Collection, Cart, CartItem, OrderItem, Review, Customer
from .pagination import DefaultPagination
from .serializers import ProductSerializer, CollectionSerializer, CustomerSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    ##### FILTER USING OVERRIDES
        # def get_queryset(self):
        #    queryset = Product.objects.all()
        #    collection_id = self.request.query_params.get('collection_id')
        #    if collection_id is not None:
        #        queryset = queryset.filter(collection_id= collection_id)
        #    return queryset
     
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, 
                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
     
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
           return Response({'error': 'Collection cannot be deleted'}, status=status.HTTP_204_NO_CONTENT)
        collection.delete()
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


    # def delete(self, request, pk):
    #    collection = get_object_or_404(Collection, pk=pk)
    #    if collection.products.count() > 0:
    #        return Response({'error': 'Collection cannot be deleted'}, status=status.HTTP_204_NO_CONTENT)
    #    collection.delete()
    #    return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('OK')

    # def get_permissions(self):
    #    if self.request.method == 'GET':
    #        return [AllowAny()]
    #    return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



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
# class CollectionList(ListCreateAPIView):
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
# class CategoryDetail(RetrieveUpdateDestroyAPIView):
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


from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
#from pprint import pprint

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
#pprint(router.urls)

### NESTED ROUTES FOR PRODUCTS REVIEWS
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
### NESTED ROUTES FOR CARTS CART-ITEMS
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = [
    # path('', include(router.urls + products_router.urls + carts_router.urls))#    path('products/', views.ProductList.as_view()),
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls)),
#    path('products/<int:pk>/', views.ProductDetail.as_view()),
#    path('collections/', views.CollectionList.as_view()),
#    path('collections/<int:pk>/', views.CategoryDetail.as_view(), name='collection-detail'),
]



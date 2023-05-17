from django.urls import path
from . import views
from rest_framework import routers


urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CategoryDetail.as_view(), name='collection-detail'),
]



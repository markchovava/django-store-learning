from django.shortcuts import render
from django.db.models import Q, F, Value, Func
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models.functions import Concat
from django.db import transaction
from django.http import HttpResponse
from store.models import Product, Customer, Collection, Order, OrderItem


# @transaction.atomic()
def say_hello(request):
    # return HttpResponse('Hello world.')
    # product = Product.objects.filter(id=1).first()
    # product = Product.objects.filter(unit_price__gt=9000).count()
    # products = Product.objects.filter(unit_price__range=(10, 70))
    # products = Product.objects.filter(inventory__lt=10, unit_price__lt=30)
    # products = Product.objects.filter(Q(inventory__lt=15) | Q(unit_price__lt=35))
    # products = Product.objects.filter(Q(inventory__lt=15) & ~Q(unit_price__lt=35)) # QUANTITY IS LESS THAN 15 AND PRICE IS NOT LESS THAN 35
    # products = Product.objects.filter(inventory=F('collection__id')) # INVENTORY QUANTITY IS EQUAL TO COLLECTION ID
    # products = Product.objects.order_by('unit_price', '-title') # order by unit price ascending and title descending
    # products = Product.objects.all()[:10] # limit to 10
    # products = Product.objects.all()[10:30] # limit from 10 to 30
    # products = Product.objects.values('id', 'title', 'collection__title') # returns specified columns only
    # products = Product.objects.select_related('collections').all() # to query related tables
    # products = Product.objects.prefetch_related('collection').filter(unit_price__range=(10, 70)).order_by('unit_price')[:10]
    # products = Product.objects.selected_related('collection').filter(unit_price__range=(10, 70)).order_by('unit_price')[:10]
    # quantity = Product.objects.aggregate(count=Count('id'), min=Min('unit_price'))
    products = Product.objects.annotate(is_new=Value(True))[:10]
    # CONCAT
    # full_name = Func(F('first_name'), Value(' ', F('last_name'), function='CONCAT')) 
    # full_name = Customer.objects.annotate(
    #    Concat('first_name', Value(' '), 'last_name' )
    # )

    # CREATES NEW OBJECT
    # collection = Collection()
    # collection.title = 'Strong'
    # collection.featured_product = Product(pk=3)
    # collection.featured_product_id = 4
    #collection.save()
    # UPDATE OBJECT
    # collection = Collection.objects.get(pk=1)
    # collection.title = 'Cereal'
    # collection.featured_product_id = 3
    # collection.save()
    # DELETE SINGLE OBJECT
    # collection = Collection.objects.get(pk=8)
    # collection.delete()
    # DELETE MULTIPLE OBJECTS
    # collection = Collection.objects.filter(id__gt=5)
    # collection.delete()

    """ with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 3
        item.unit_price = 7.43
        item.save() """

    context = { 
        'name': 'Mark Chovava',
        'products': products
        }
    return render(request, 'index.html', context)

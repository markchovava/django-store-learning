from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product

 
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    min_num = 1
    extra = 0


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
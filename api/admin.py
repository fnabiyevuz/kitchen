from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group

admin.site.site_header = "Kitchen Admin Panel"
admin.site.site_title = "Kitchen API"
admin.site.index_title = "Kitchen API"

# admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(SalesTypes)
class SalesTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')
    list_display_links = ('id', 'type')


@admin.register(Busytype)
class BusytypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'price')
    list_display_links = ('id', 'type', 'price')


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'password', 'unity', 'salary', 'position', 'number')
    list_display_links = ('id', 'first_name', 'last_name')


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'salestype', 'status', 'unitysalary', 'number')
    list_display_links = ('id', 'name',)


@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'room')
    list_display_links = ('id', 'name',)
    list_filter = ('status',)


@admin.register(Recieve)
class RecieveAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'summa')
    list_display_links = ('id', 'date')


@admin.register(RecieveItems)
class RecieveItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price', 'comment')
    list_display_links = ('id', 'product')


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'waiter', 'status', 'total', 'total_amount',  'busyprice', 'room', 'date')
    list_display_links = ('id', 'waiter')
    list_filter = ('waiter', 'room', 'status')
    date_hierarchy = 'date'


@admin.register(BooksItems)
class BooksItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'product', 'cook', 'quantity', 'status', 'price')
    list_display_links = ('id', 'book')


@admin.register(WaitersBook)
class WaitersBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'status', 'date')
    list_display_links = ('id', 'user')
    list_filter = ('user', 'product')
    date_hierarchy = 'date'

@admin.register(Chiqim)
class ChiqimAdmin(admin.ModelAdmin):
    list_display = ('id', 'summa', 'comment', 'date')
    list_display_links = ('id', 'summa')
    date_hierarchy = 'date'


@admin.register(ServiceFee)
class ServiceFeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'percent')
    list_display_links = ('id', 'percent')


@admin.register(Busy)
class BusyAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'phone', 'room', 'date', 'status')
    list_display_links = ('id', 'fio')

@admin.register(Saboy)
class SaboyAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'phone', 'total', 'date', 'status')
    list_display_links = ('id', 'fio')
    date_hierarchy = 'date'

@admin.register(SaboyItem)
class SaboyItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'saboy', 'product', 'cook', 'quantity', 'status')
    list_display_links = ('id', 'saboy')


@admin.register(BuyurtmaSetting)
class BuyurtmaSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'qozon_haqi', 'kishi_boshi')
    list_display_links = ('id', 'qozon_haqi')

@admin.register(Buyurtma)
class BuyurtmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'cook', 'people', 'total', 'products', 'status', 'datetime')
    list_display_links = ('id', 'book')

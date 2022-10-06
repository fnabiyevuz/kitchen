from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'phone', 'position', 'number', 'password']


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class ProductsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'picture', 'number']

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'


class RecieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recieve
        fields = '__all__'


class RecieveItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecieveItems
        fields = '__all__'


class BooksReadSerializer(serializers.ModelSerializer):
    waiter = UsersSerializer(read_only=True)
    room = RoomsSerializer(read_only=True)

    class Meta:
        model = Books
        fields = '__all__'


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class BooksItemsSerializer(serializers.ModelSerializer):
    # book = BooksSerializer(read_only=True)
    # cook = UsersSerializer(read_only=True)
    product = ProductsItemSerializer(read_only=True)

    class Meta:
        model = BooksItems
        fields = '__all__'


class BusytypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busytype
        fields = '__all__'


class ChiqimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chiqim
        fields = '__all__'


class WaitersBookSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)

    class Meta:
        model = WaitersBook
        fields = '__all__'


class BusySerializer(serializers.ModelSerializer):
    class Meta:
        model = Busy
        fields = '__all__'


class SaboySerializer(serializers.ModelSerializer):
    class Meta:
        model = Saboy
        fields = '__all__'


class SaboyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaboyItem
        fields = '__all__'


class BuyurtmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyurtma
        fields = '__all__'

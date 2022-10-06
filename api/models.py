from django.db import models


class SalesTypes(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = 'SalesTypes'


class Busytype(models.Model):
    type = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.type)

    class Meta:
        verbose_name_plural = 'BusyTypes'


class Products(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='picture/', null=True, blank=True)
    price = models.IntegerField(null=True)
    quantity = models.FloatField(null=True)
    salestype = models.ForeignKey(SalesTypes, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(default=0)
    unitysalary = models.IntegerField(default=0)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Products'


class Users(models.Model):
    sts = (
        (1, 'director'),
        (2, 'cashier'),
        (3, 'cook'),
        (4, 'warehouseman'),
        (5, 'waiter'),
        (6, 'delivery'),
        (7, 'orderdeliver'),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255, unique=True)
    unity = models.IntegerField(default=0)
    salary = models.IntegerField(default=0)
    position = models.IntegerField(choices=sts, default=5)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name_plural = 'Users'


class Rooms(models.Model):
    name = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    room = models.BooleanField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Rooms'


class Recieve(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    summa = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name_plural = 'Recieve'


class RecieveItems(models.Model):
    recieve = models.ForeignKey(Recieve, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField(null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    comment = models.TextField()

    def __str__(self):
        return str(self.recieve_id)

    class Meta:
        verbose_name_plural = 'RecieveItems'


class Books(models.Model):
    waiter = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='waiter')
    room = models.ForeignKey(Rooms, models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    busyprice = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Books'


class BooksItems(models.Model):
    book = models.ForeignKey(Books, on_delete=models.SET_NULL, null=True)
    cook = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField(default=0)
    price = models.FloatField(null=True, blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'BooksItems'


class WaitersBook(models.Model):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=0)

    # def __str__(self):
    #         return self.date

    class Meta:
        verbose_name_plural = 'WaitersBook'


class BusyRooms(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    fio = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return self.room.name

    class Meta:
        verbose_name_plural = 'BusyRooms'


class Chiqim(models.Model):
    summa = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.summa)

    class Meta:
        verbose_name_plural = 'Chiqimlar'


class ServiceFee(models.Model):
    percent = models.FloatField(default=10)

    def __str__(self):
        return str(self.percent)

    class Meta:
        verbose_name_plural = 'Xona xizmati foizda'


class Busy(models.Model):
    fio = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name_plural = 'Band'


class Saboy(models.Model):
    fio = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    total = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Saboy'


class SaboyItem(models.Model):
    saboy = models.ForeignKey(Saboy, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cook = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField()
    quantity = models.FloatField()
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'Saboyitem'


class BuyurtmaSetting(models.Model):
    qozon_haqi = models.IntegerField(default=0)
    kishi_boshi = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'BuyurtmaSetting'

class Buyurtma(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    cook = models.ForeignKey(Users, on_delete=models.CASCADE)
    people = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    products = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Buyurtma'
from rest_framework import viewsets
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import json
from django.db.models import Sum, Count, F


class UsersViewset(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):
        if request.method == "POST":
            password = request.data['password']
            try:
                user = Users.objects.get(password=password)
                d = self.get_serializer_class()(user)
                return Response({'user': d.data}, status=200)
            except:
                return Response({'message': 'user not found'}, status=204)
        else:
            return Response()

    @action(methods=['post'], detail=False)
    def pay(self, request):
        user = request.data['user']
        summa = request.data['summa']
        u = Users.objects.get(id=user)
        u.salary -= summa
        u.save()
        dt = self.get_serializer_class()(u).data
        return Response(dt)


class ProductsViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        prod = Products.objects.filter(status=0)

        dt = self.get_serializer_class()(prod, many=True).data
        return Response(dt)

    @action(methods=['post'], detail=False)
    def add(self, request):
        id = request.data['product']
        quan = request.data['quantity']

        prod = Products.objects.get(id=id)
        prod.quantity += float(quan)
        prod.save()

        dt = self.get_serializer_class()(prod).data
        return Response(dt)


class RoomsViewset(viewsets.ModelViewSet):
    queryset = Rooms.objects.all()
    serializer_class = RoomsSerializer


class RecieveViewset(viewsets.ModelViewSet):
    queryset = Recieve.objects.all()
    serializer_class = RecieveSerializer


class RecieveItemsViewset(viewsets.ModelViewSet):
    queryset = RecieveItems.objects.all()
    serializer_class = RecieveItemsSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        if request.method == "POST":
            r = request.data
            recieveitems = r['recieveitems']
            summa = 0
            date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
            try:
                rec = Recieve.objects.filter(date__gte=date).last()
            except:
                rec = Recieve.objects.create()
            for item in recieveitems:
                RecieveItems.objects.create(recieve=rec, product_id=item['product'], quantity=item['quantity'],
                                            price=item['price'])
                prod = Products.objects.get(id=item['product'])
                prod.quantity += item['quantity']
                prod.save()
                summa += item['price'] * item['quantity']
            rec.summa += summa
            rec.save()
            return Response({'message': 'done'}, status=201)
        else:
            return Response()

    @action(methods=['post'], detail=False)
    def pay_salary(self, request):
        if request.method == "POST":
            r = request.data
            comment = r['comment']
            price = r['price']
            date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
            try:
                rec = Recieve.objects.filter(date__gte=date).last()
            except:
                rec = Recieve.objects.create()
            item = RecieveItems.objects.create(recieve=rec, comment=comment, price=price)
            dt = self.get_serializer_class()(item).data
            return Response(dt)


class BooksViewset(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    @action(methods=['get'], detail=False)
    def book0(self, request):
        books = Books.objects.filter(status=0)
        dt = BooksReadSerializer(books, many=True)

        return Response(dt.data)

    @action(methods=['post'], detail=False)
    def by_range(self, request):
        r = request.data
        date1 = r['date1']
        try:
            date2 = r['date2']
            books = Books.objects.filter(date__gte=date1, date__lt=date2)
        except:
            books = Books.objects.filter(date__gte=date1)
        dt = BooksReadSerializer(books, many=True)
        return Response(dt.data)

    @action(methods=['get'], detail=False)
    def bugunlik(self, req):
        date = datetime.today()
        dt = datetime(date.year, date.month, date.day)

        b = Books.objects.filter(date__gte=dt, status=1)
        s = Saboy.objects.filter(date__gte=dt, status=1)
        buyurt = Buyurtma.objects.filter(datetime__gte=dt, status=1)
        ch = Chiqim.objects.filter(date__gte=dt)

        total = b.aggregate(Sum('total'))['total__sum']
        if total is None:
            total = 0
        stotal = s.aggregate(Sum('total'))['total__sum']
        if stotal is None:
            stotal = 0
        dtotal = d.aggregate(Sum('total'))['total__sum']
        if dtotal is None:
            dtotal = 0
        buyurttotal = buyurt.aggregate(Sum('total'))['total__sum']
        if buyurttotal is None:
            buyurttotal = 0
        chiqim = ch.aggregate(Sum('summa'))['summa__sum']
        if chiqim is None:
            chiqim = 0
        total_amount = b.aggregate(Sum('total_amount'))['total_amount__sum']
        if total_amount is None:
            total_amount = 0
        # bk = BooksSerializer(b, many=True).data
        # chk = ChiqimSerializer(ch, many=True).data
        return Response({
            'book_total': total,
            'saboy_total': stotal,
            'buyurtma_total': buyurttotal,
            'chiqim': chiqim,
            'service_sum': total_amount,
        })


class BooksItemsViewset(viewsets.ModelViewSet):
    queryset = BooksItems.objects.all()
    serializer_class = BooksItemsSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        if request.method == "POST":
            r = request.data
            waiter = r['waiter']
            room = r['room']
            bookitems = r['bookitems']
            book = Books.objects.create(waiter_id=waiter, room_id=room)
            for item in bookitems:
                BooksItems.objects.create(book=book, product_id=item['product'], quantity=item['quantity'])
            return Response({'message': 'done'}, status=201)
        else:
            return Response()

    @action(methods=['get'], detail=False)
    def by_book(self, request):
        id = request.GET.get('b')
        items = BooksItems.objects.filter(book_id=id)
        dt = self.get_serializer_class()(items, many=True)

        return Response(dt.data)

    @action(methods=['get'], detail=False)
    def bugunlik(self, req):
        date = datetime.today()
        dt = datetime(date.year, date.month, date.day)
        response_data = list(BooksItems.objects.filter(book__date__gte=dt)
            .values('product__name').annotate(
            count=Count(F('id')),
            quantity=Sum(F('quantity')),
            price=Sum(F('price'))
        ))
        return Response(response_data)

class ChiqimViewset(viewsets.ModelViewSet):
    queryset = Chiqim.objects.all()
    serializer_class = ChiqimSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        data = request.data
        summa = data['summa']
        comment = data['comment']
        ch = Chiqim.objects.create(summa=summa, comment=comment)
        dt = self.get_serializer_class()(ch).data

        return Response(dt)

    @action(methods=['get'], detail=False)
    def bugunlik(self, request):
        today = datetime.today()
        date1 = datetime(today.year, today.month, today.day)
        result = Chiqim.objects.filter(date__gte=date1)
        chiqim = result.aggregate(Sum('summa'))['summa__sum']
        res = self.get_serializer_class()(result, many=True).data
        # dt = ChiqimSerializer(books, many=True)
        return Response({'total_chiqim': chiqim, 'result': res})

    @action(methods=['post'], detail=False)
    def oylik(self, request):
        r = request.data
        id = r['id']
        summa = r['summa']
        comment = r['comment']
        Chiqim.objects.create(summa=summa, comment=comment)

        u = Users.objects.get(id=id)
        u.salary -= summa
        u.save()
        dt = UsersSerializer(u).data
        return Response(dt)

    @action(methods=['post'], detail=False)
    def by_range(self, request):
        r = request.data
        date1 = r['date1']
        try:
            date2 = r['date2']
            books = Chiqim.objects.filter(date__gte=date1, date__lt=date2)
        except:
            books = Chiqim.objects.filter(date__gte=date1)
        dt = ChiqimSerializer(books, many=True)
        return Response(dt.data)


class BusyViewset(viewsets.ModelViewSet):
    queryset = Busy.objects.all()
    serializer_class = BusySerializer


class BusytypeViewset(viewsets.ModelViewSet):
    queryset = Busytype.objects.all()
    serializer_class = BusytypeSerializer


class SaboyViewset(viewsets.ModelViewSet):
    queryset = Saboy.objects.all()
    serializer_class = SaboySerializer


class SaboyItemViewset(viewsets.ModelViewSet):
    queryset = SaboyItem.objects.all()
    serializer_class = SaboyItemSerializer




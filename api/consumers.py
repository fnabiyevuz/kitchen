import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .serializers import *


class RoomsSocket(AsyncWebsocketConsumer):

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'rooms'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.RecieveData(data)
        dt = await self.AllData()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room',
                'data': dt
            }
        )

    # Receive message from room group
    async def room(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['data']))

    async def RecieveData(self, data):
        if data['type'] == "alldata":
            data['data'] = await self.AllData()
        elif data['type'] == "busy1":
            data['data'] = await self.busy1(data['data'])
        elif data['type'] == "busy0":
            data['data'] = await self.busy0(data['id'])
        elif data['type'] == "bookitemadd":
            data['data'] = await self.bookitemadd(data['data'])
        elif data['type'] == "bookitem1":
            data['data'] = await self.bookitem1(data['data'])
        elif data['type'] == "bookitem2":
            data['data'] = await self.bookitem2(data['data'])
        elif data['type'] == "bookwaiter":
            data['data'] = await self.bookwaiter(data['data'])
        # elif data['type'] == "pay":
        #     data['data'] = await self.pay(data['data'])
        elif data['type'] == "deleteitem":
            data['data'] = await self.deleteitem(data['id'])
        elif data['type'] == "avvaldanbandqilish":
            data['data'] = await self.avvaldanbandqilish(data['data'])
        elif data['type'] == "createsaboy":
            data['data'] = await self.createsaboy(data['data'])
        elif data['type'] == "saboyitemadd":
            data['data'] = await self.saboyitemadd(data['data'])
        elif data['type'] == "saboyitemdelete":
            data['data'] = await self.saboyitemdelete(data['id'])
        elif data['type'] == "saboychangestatus":
            data['data'] = await self.saboychangestatus(data['id'])
        elif data['type'] == "buyurtma":
            data['data'] = await self.buyurtma(data['data'])
        elif data['type'] == "buyurtmaitemchangestatus":
            data['data'] = await self.buyurtmaitemchangestatus(data['id'])

        return data

    @database_sync_to_async
    def AllData(self):
        room0 = Rooms.objects.filter(status=0)
        room1 = Rooms.objects.filter(status=1)
        users = Users.objects.all()
        products = Products.objects.all()
        books = Books.objects.filter(status=0)
        saboy = Saboy.objects.filter(status=0)
        booksitems = BooksItems.objects.filter(book__status=0)
        busytypes = Busytype.objects.all()
        wb = WaitersBook.objects.filter(status=0)
        bb = []
        ss = []
        boks = []
        for s in saboy:
            i0 = []
            items = SaboyItem.objects.filter(saboy=s)
            for i in items:
                d = {
                    'id': i.id,
                    'product': i.product.name,
                    'quantity': i.quantity,
                    'price': i.price,
                    'product_status': i.product.status,
                    'status': i.status,
                }
                i0.append(d)
            t = {
                'saboy': s.id,
                'fio': s.fio,
                'items': i0,
                'phone': s.phone,
                'date': s.date.strftime("%Y-%m-%d %H:%M")
            }
            ss.append(t)

        for b in books:
            items = BooksItems.objects.filter(book=b)
            i0 = []
            m = 0
            n = 0
            for i in items:
                d = {
                    'id': i.id,
                    'number': i.product.number,
                    'product': i.product.name,
                    'quantity': i.quantity,
                    'price': i.product.price * i.quantity,
                    'status': i.product.status,
                }
                i0.append(d)
                if i.product.status == 1:
                    m += 1
                if i.product.status == 0:
                    n += 1
            t = {
                'book': b.id,
                'room': b.room.id,
                'waiter': b.waiter.id,
                'total': b.total,
                'total_amount': b.total_amount,
                'busyprice': b.busyprice,
                'bookitems': i0
            }
            bb.append(t)
            waiter = Users.objects.get(id=b.waiter.id)
            w = {
                'id': waiter.id,
                'first_name': waiter.first_name,
                'last_name': waiter.last_name,
            }
            room = Rooms.objects.get(id=b.room.id)
            ro = {
                'id': room.id,
                'name': room.name
            }
            if m == 0 and n > 0:
                bbb = {
                    'id': b.id,
                    'waiter': w,
                    'room': ro,
                    'date': b.date.strftime("%Y-%m-%d %H:%M"),
                    'total': b.total,
                    'status': b.status,
                    'busyprice': b.busyprice,
                    'total_amount': b.total_amount,
                    'kitchen': False,
                    'warehause': True
                }
            elif m > 0 and n == 0:
                bbb = {
                    'id': b.id,
                    'waiter': w,
                    'room': ro,
                    'date': b.date.strftime("%Y-%m-%d %H:%M"),
                    'total': b.total,
                    'status': b.status,
                    'busyprice': b.busyprice,
                    'total_amount': b.total_amount,
                    'kitchen': True,
                    'warehause': False
                }
            else:
                bbb = {
                    'id': b.id,
                    'waiter': w,
                    'room': ro,
                    'date': b.date.strftime("%Y-%m-%d %H:%M"),
                    'total': b.total,
                    'status': b.status,
                    'busyprice': b.busyprice,
                    'total_amount': b.total_amount,
                    'kitchen': True,
                    'warehause': True
                }

            boks.append(bbb)
        buyurt = Buyurtma.objects.filter(status=0)

        return {
            'type': 'alldata',
            'room0': RoomsSerializer(room0, many=True).data,
            'room1': RoomsSerializer(room1, many=True).data,
            'users': UsersSerializer(users, many=True).data,
            'products': ProductsSerializer(products, many=True).data,
            'books': boks,
            'booksitems': BooksItemsSerializer(booksitems, many=True).data,
            'bookswithitems': bb,
            'saboywithitems': ss,
            'busytypes': BusytypeSerializer(busytypes, many=True).data,
            'waiterbook': WaitersBookSerializer(wb, many=True).data,
            'buyurtma': BuyurtmaSerializer(buyurt, many=True).data
        }

    @database_sync_to_async
    def busy1(self, data):
        room = Rooms.objects.get(id=data['id'])
        if room.status == 0:
            room.status = 1
            room.save()
            type = Busytype.objects.get(id=data['busytype'])
            per = ServiceFee.objects.first()
            Books.objects.create(waiter_id=data['waiter'], busyprice=type.price, room_id=data['id'], total=type.price)

            return

    @database_sync_to_async
    def busy0(self, id):
        room = Rooms.objects.get(id=id)
        room.status = 0
        room.save()
        book = Books.objects.get(room_id=room, status=0)
        try:
            per = ServiceFee.objects.first()
            book.total_amount = per.percent * (book.total) / 100
        except:
            book.total_amount = 0.1 * (book.total)
        items = BooksItems.objects.filter(book=book, status=0)
        for i in items:
            if i.product.salestype.type == 'kg':
                i.product.quantity -= i.quantity
                i.product.save()
            elif i.product.salestype.type == 'dona':
                i.product.quantity -= i.quantity
                i.product.save()
        book.status = 1
        book.save()

        return

    @database_sync_to_async
    def bookitemadd(self, data):
        bitem = BooksItems.objects.create(book_id=data['book'], product_id=data['product'], quantity=data['quantity'])
        books = Books.objects.get(id=data['book'])
        per = ServiceFee.objects.first()
        b = Products.objects.get(id=data['product'])
        if b.status == 0:
            books.total += data['quantity'] * b.price
            bitem.price = data['quantity'] * b.price
            bitem.save()
        else:
            if b.salestype.type == 'kg':
                books.total += data['quantity'] * b.price
                bitem.price = data['quantity'] * b.price
                bitem.save()
            elif b.salestype.type == 'qozon':
                if data['quantity'] == 0.6:
                    books.total += b.price
                    bitem.price = b.price
                    bitem.save()
                elif data['quantity'] == 0.8:
                    books.total += b.price
                    bitem.price = b.price
                    bitem.save()
                else:
                    books.total += b.price * data['quantity']
                    bitem.price = b.price * data['quantity']
                    bitem.save()
            elif b.salestype.type == 'dona':
                books.total += b.price * data['quantity']
                bitem.price = b.price * data['quantity']
                bitem.save()
        books.total_amount = (books.total - books.busyprice) * per.percent / 100
        books.save()

        return

    @database_sync_to_async
    def bookitem1(self, data):
        item = BooksItems.objects.get(id=data['id'])
        try:
            item.cook_id = data['cook']
            cook = Users.objects.get(id=data['cook'])
            if item.product.salestype.type == 'qozon':
                cook.salary += cook.unity
            elif item.product.salestype.type == 'kg':
                cook.salary += item.quantity * cook.unity
                item.product.quantity -= item.quantity
                item.product.save()
            else:
                cook.salary += item.quantity * cook.unity
            cook.save()
        except:
            item.cook_id = data['warehause']
            item.product.quantity -= item.quantity
            item.product.save()
        item.status = 1
        item.save()
        return

    @database_sync_to_async
    def bookitem2(self, data):
        item = BooksItems.objects.get(id=data['id'])
        item.status = 2
        item.save()
        return

    @database_sync_to_async
    def bookwaiter(self, data):
        WaitersBook.objects.create(user_id=data['user'], product_id=data['product'], quantity=data['quantity'])

    @database_sync_to_async
    def deleteitem(self, id):
        percent = ServiceFee.objects.first()
        i = BooksItems.objects.get(id=id)
        if i.product.status == 0:
            i.book.total -= i.product.price * i.quantity
            i.book.total_amount = (i.book.total - i.book.busyprice) * percent.percent / 100
            i.product.quantity += i.quantity
            i.book.save()
            i.product.save()
        elif i.product.salestype.type == "kg":
            i.book.total -= i.quantity * i.product.price
            i.book.total_amount = (i.book.total - i.book.busyprice) * percent.percent / 100
            i.product.quantity += i.quantity
            i.book.save()
        elif i.product.salestype.type == 'qozon':
            if i.quantity >= 1:
                i.book.total = i.book.total - i.product.price * i.quantity
            else:
                i.book.total = i.book.total - i.product.price
            i.book.total_amount = (i.book.total - i.book.busyprice) * percent.percent / 100
            i.book.save()
        i.delete()

        return

    @database_sync_to_async
    def avvaldanbandqilish(self, data):
        fio = data['fio']
        phone = data['phone']
        room = data['room']
        date = data['date']
        Busy.objects.create(fio=fio, phone=phone, room_id=room, date=date)

        return

    @database_sync_to_async
    def createsaboy(self, data):
        fio = data['fio']
        phone = data['phone']
        Saboy.objects.create(fio=fio, phone=phone)

        return

    @database_sync_to_async
    def saboyitemadd(self, data):
        saboy = data['saboy']
        product = data['product']
        quantity = data['quantity']
        sab = Saboy.objects.get(id=saboy)
        b = Products.objects.get(id=data['product'])
        if b.status == 0:
            sab.total += data['quantity'] * b.price
            price = data['quantity'] * b.price
        else:
            if b.salestype.type == 'kg':
                sab.total += data['quantity'] * b.price
                price = data['quantity'] * b.price
            elif b.salestype.type == 'qozon':
                if data['quantity'] == 0.6:
                    sab.total += b.price
                    price = b.price
                elif data['quantity'] == 0.8:
                    sab.total += b.price
                    price = b.price
                else:
                    sab.total += b.price * data['quantity']
                    price = b.price * data['quantity']
            elif b.salestype.type == 'dona':
                sab.total += b.price * data['quantity']
                price = b.price * data['quantity']
        sab.save()
        SaboyItem.objects.create(saboy_id=saboy, price=price, product_id=product, quantity=quantity)

        return

    @database_sync_to_async
    def saboyitemdelete(self, id):
        item = SaboyItem.objects.get(id=id)
        item.saboy.total -= item.price
        item.saboy.save()
        item.delete()

        return

    @database_sync_to_async
    def saboychangestatus(self, id):
        d = Saboy.objects.get(id=id)
        d.status = 1
        d.save()

        return

    @database_sync_to_async
    def buyurtma(self, data):
        set = BuyurtmaSetting.objects.first()
        Buyurtma.objects.create(book_id=data['book'], cook_id=data['cook'], people=int(data['people']),
                                total=int(data['people']) * set.kishi_boshi + set.qozon_haqi, products=data['products'])
        return

    @database_sync_to_async
    def buyurtmaitemchangestatus(self, id):
        buyurt = Buyurtma.objects.get(id=id)
        buyurt.status = 1
        buyurt.save()

        return


class RoomSocket(AsyncWebsocketConsumer):

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'rooms'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.RecieveData(data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room',
                'data': await self.Rooms()
            }
        )

    # Receive message from room group
    async def room(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['data']))

    async def RecieveData(self, data):
        if data['type'] == "rooms":
            # data['data'] = await self.Rooms()
            pass
        elif data['type'] == "busy1":
            data['data'] = await self.busy1(data['data'])
        elif data['type'] == "busy0":
            data['data'] = await self.busy0(data['id'])

        return data

    @database_sync_to_async
    def Rooms(self):
        room1 = Rooms.objects.filter(status=1)
        room0 = Rooms.objects.filter(status=0)
        r1 = RoomsSerializer(room1, many=True).data
        r0 = RoomsSerializer(room0, many=True).data
        data = {
            'room1': r1,
            'room0': r0
        }
        return data

    @database_sync_to_async
    def busy1(self, data):
        room = Rooms.objects.get(id=data['id'])
        if room.status == 0:
            books = Books.objects.filter(room=room, status=0)
            for b in books:
                b.status = 1
                b.save()
            room.status = 1
            room.save()
            type = Busytype.objects.get(id=data['busytype'])
            Books.objects.create(waiter_id=data['waiter'], busyprice=type.price, room_id=data['id'], total=type.price)

            return

    @database_sync_to_async
    def busy0(self, id):
        room = Rooms.objects.get(id=id)
        room.status = 0
        room.save()
        book = Books.objects.get(room_id=room, status=0)
        try:
            per = ServiceFee.objects.first()
            book.total_amount = per.percent * (book.total) / 100
        except:
            book.total_amount = 0.1 * (book.total)
        items = BooksItems.objects.filter(book=book, status=0)
        for i in items:
            if i.product.salestype.type == 'kg':
                i.product.quantity -= i.quantity
                i.product.save()
            elif i.product.salestype.type == 'dona':
                i.product.quantity -= i.quantity
                i.product.save()
        book.status = 1
        book.save()


class BookSocket(AsyncWebsocketConsumer):

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'book'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.RecieveData(data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room',
                'data': await self.Book()
            }
        )

    # Receive message from room group
    async def room(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['data']))

    async def RecieveData(self, data):
        if data['type'] == "book":
            data['data'] = await self.Book()

        return data

    @database_sync_to_async
    def Book(self):
        books = BooksItems.objects.filter(status=0)
        for b in books:
            b.status = 1
            b.save()
        bb = []
        boks = []
        books = Books.objects.filter(room__status=1)
        for b in books:
            items = BooksItems.objects.filter(book=b)
            i0 = []
            m = 0
            n = 0
            for i in items:
                d = {
                    'id': i.id,
                    'number': i.product.number,
                    'product': i.product.name,
                    'quantity': i.quantity,
                    'price': i.product.price * i.quantity,
                    'status': i.product.status,
                }
                i0.append(d)
                if i.product.status == 1:
                    m += 1
                if i.product.status == 0:
                    n += 1
            t = {
                'book': b.id,
                'room': b.room.id,
                'waiter': b.waiter.id,
                'total': b.total,
                'total_amount': b.total_amount,
                'busyprice': b.busyprice,
                'bookitems': i0
            }
            bb.append(t)
            waiter = Users.objects.get(id=b.waiter.id)
            w = {
                'id': waiter.id,
                'first_name': waiter.first_name,
                'last_name': waiter.last_name,
            }
            room = Rooms.objects.get(id=b.room.id)
            ro = {
                'id': room.id,
                'name': room.name
            }
            if m == 0 and n > 0:
                b = {
                    'id': b.id,
                    'waiter': w,
                    'room': ro,
                    'date': b.date.strftime("%Y-%m-%d %H:%M"),
                    'total': b.total,
                    'status': b.status,
                    'busyprice': b.busyprice,
                    'total_amount': b.total_amount,
                    'kitchen': False,
                    'warehause': True
                }
            elif m > 0 and n == 0:
                b = {
                    'id': b.id,
                    'waiter': w,
                    'room': ro,
                    'date': b.date.strftime("%Y-%m-%d %H:%M"),
                    'total': b.total,
                    'status': b.status,
                    'busyprice': b.busyprice,
                    'total_amount': b.total_amount,
                    'kitchen': True,
                    'warehause': False
                }
            else:
                b = {
                    'id': b.id,
                    'waiter': w,
                    'room': ro,
                    'date': b.date.strftime("%Y-%m-%d %H:%M"),
                    'total': b.total,
                    'status': b.status,
                    'busyprice': b.busyprice,
                    'total_amount': b.total_amount,
                    'kitchen': True,
                    'warehause': True
                }

            boks.append(b)
        dt = {
            'books': boks,
        }
        return dt


def spl(room):
    name = room.split('_')
    return name


@database_sync_to_async
def Number(number):
    items = BooksItems.objects.filter(book__status=0, status=0, product__number=number)
    dt = BooksItemsSerializer(items, many=True).data
    return dt


class RoomItemSocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.RecieveData(data)
        # await self.send(text_data=json.dumps(send_data))

        number = send_data['data'][-1:][0]['product']['number']
        if self.room_group_name == 'room_cook_{}'.format(number):
            send_data = await Number(number)
            await self.channel_layer.group_send(
                'room_cook_{}'.format(number),
                {
                    'type': 'room',
                    'data': send_data
                }
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room',
                    'data': send_data
                }
            )
            send_data = await Number(number)
            await self.channel_layer.group_send(
                'room_cook_{}'.format(number),
                {
                    'type': 'room',
                    'data': send_data
                }
            )
    # Receive message from room group
    async def room(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['data']))

    async def RecieveData(self, data):
        if data['type'] == "roomitem":
            data['data'] = await self.RoomItem()
        elif data['type'] == "addbookitem":
            data['data'] = await self.AddBookItem(data['data'])
        elif data['type'] == "cookitem":
            data['data'] = await self.CookItem()
        elif data['type'] == "cookchangeitem":
            data['data'] = await self.CookChangeItem(data['id'])

        return data

    @database_sync_to_async
    def RoomItem(self):
        items = BooksItems.objects.filter(book__room_id=self.room_name, book__status=0)
        dt = BooksItemsSerializer(items, many=True).data
        return dt

    @database_sync_to_async
    def AddBookItem(self, data):
        books = Books.objects.get(room_id=self.room_name, status=0)
        bitem = BooksItems.objects.create(book=books, product_id=data['product'], quantity=data['quantity'])
        # books = Books.objects.get(id=data['book'])
        per = ServiceFee.objects.first()
        b = Products.objects.get(id=data['product'])
        if b.status == 0:
            books.total += data['quantity'] * b.price
            bitem.price = data['quantity'] * b.price
            bitem.save()
        else:
            if b.salestype.type == 'kg':
                books.total += data['quantity'] * b.price
                bitem.price = data['quantity'] * b.price
                bitem.save()
            elif b.salestype.type == 'qozon':
                if data['quantity'] == 0.6:
                    books.total += b.price
                    bitem.price = b.price
                    bitem.save()
                elif data['quantity'] == 0.8:
                    books.total += b.price
                    bitem.price = b.price
                    bitem.save()
                else:
                    books.total += b.price * data['quantity']
                    bitem.price = b.price * data['quantity']
                    bitem.save()
            elif b.salestype.type == 'dona':
                books.total += b.price * data['quantity']
                bitem.price = b.price * data['quantity']
                bitem.save()
        books.total_amount = (books.total - books.busyprice) * per.percent / 100
        books.save()
        items = BooksItems.objects.filter(book=books, book__room=self.room_name, book__status=0)
        dt = BooksItemsSerializer(items, many=True).data

        return dt

    @database_sync_to_async
    def CookItem(self):
        r = spl(self.room_name)
        items = BooksItems.objects.filter(book__status=0, status=0, product__number=r[1])
        dt = BooksItemsSerializer(items, many=True).data
        return dt

    @database_sync_to_async
    def CookChangeItem(self, id):
        item = BooksItems.objects.get(id=id)
        item.status = 1
        item.save()
        return


class CookSocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.RecieveData(data)
        await self.send(text_data=json.dumps(send_data))

    async def RecieveData(self, data):
        if data['type'] == "cookitem":
            data['data'] = await self.CookItem()

        return data

    @database_sync_to_async
    def CookItem(self):
        items = BooksItems.objects.filter(book__status=0, status=0, product__number=self.room_name)
        dt = BooksItemsSerializer(items, many=True).data

        return dt

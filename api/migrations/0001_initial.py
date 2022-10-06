# Generated by Django 3.1.7 on 2021-06-03 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('total', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('busyprice', models.IntegerField(default=0)),
                ('total_amount', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.CreateModel(
            name='Busytype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'BusyTypes',
            },
        ),
        migrations.CreateModel(
            name='BuyurtmaSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qozon_haqi', models.IntegerField(default=0)),
                ('kishi_boshi', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'BuyurtmaSetting',
            },
        ),
        migrations.CreateModel(
            name='Chiqim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summa', models.IntegerField()),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Chiqimlar',
            },
        ),
        migrations.CreateModel(
            name='Dastavka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=13)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('total', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Dastavka',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='picture/')),
                ('price', models.IntegerField(null=True)),
                ('quantity', models.FloatField(null=True)),
                ('status', models.IntegerField(default=0)),
                ('unitysalary', models.IntegerField(default=0)),
                ('number', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Recieve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('summa', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Recieve',
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0)),
                ('room', models.BooleanField(default=1)),
            ],
            options={
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Saboy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=13)),
                ('total', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Saboy',
            },
        ),
        migrations.CreateModel(
            name='SalesTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'SalesTypes',
            },
        ),
        migrations.CreateModel(
            name='ServiceFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField(default=10)),
            ],
            options={
                'verbose_name_plural': 'Xona xizmati foizda',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255, unique=True)),
                ('unity', models.IntegerField(default=0)),
                ('salary', models.IntegerField(default=0)),
                ('position', models.IntegerField(choices=[(1, 'director'), (2, 'cashier'), (3, 'cook'), (4, 'warehouseman'), (5, 'waiter'), (6, 'delivery'), (7, 'orderdeliver')], default=5)),
                ('number', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='WaitersBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.products')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.users')),
            ],
            options={
                'verbose_name_plural': 'WaitersBook',
            },
        ),
        migrations.CreateModel(
            name='SaboyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('quantity', models.FloatField()),
                ('status', models.IntegerField(default=0)),
                ('cook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.users')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.products')),
                ('saboy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.saboy')),
            ],
            options={
                'verbose_name_plural': 'Saboyitem',
            },
        ),
        migrations.CreateModel(
            name='RecieveItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, default=0, null=True)),
                ('comment', models.TextField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.products')),
                ('recieve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.recieve')),
            ],
            options={
                'verbose_name_plural': 'RecieveItems',
            },
        ),
        migrations.AddField(
            model_name='products',
            name='salestype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.salestypes'),
        ),
        migrations.CreateModel(
            name='DastavkaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('price', models.IntegerField()),
                ('status', models.IntegerField(default=0)),
                ('cook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.users')),
                ('dastavka', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dastavka')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.products')),
            ],
            options={
                'verbose_name_plural': 'Dastavkaitem',
            },
        ),
        migrations.CreateModel(
            name='Buyurtma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('products', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.books')),
                ('cook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.users')),
            ],
            options={
                'verbose_name_plural': 'Buyurtma',
            },
        ),
        migrations.CreateModel(
            name='BusyRooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.rooms')),
            ],
            options={
                'verbose_name_plural': 'BusyRooms',
            },
        ),
        migrations.CreateModel(
            name='Busy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=13)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.rooms')),
            ],
            options={
                'verbose_name_plural': 'Band',
            },
        ),
        migrations.CreateModel(
            name='BooksItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('price', models.FloatField(blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.books')),
                ('cook', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.users')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.products')),
            ],
            options={
                'verbose_name_plural': 'BooksItems',
            },
        ),
        migrations.AddField(
            model_name='books',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.rooms'),
        ),
        migrations.AddField(
            model_name='books',
            name='waiter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='waiter', to='api.users'),
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-28 17:41

import shortuuid.django_fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=5, max_length=20, prefix='CARD', unique=True)),
                ('name', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('cvv', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('card_type', models.CharField(choices=[('master', 'master'), ('visa', 'visa'), ('verve', 'verve')], default='master', max_length=20)),
                ('card_status', models.BooleanField(default=True)),
                ('daet', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='evidences/')),
                ('reviewed', models.BooleanField(default=False)),
                ('validated', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EvidenceWithPersons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='evidences_persons/')),
                ('deposit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('validated', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('ticket_number', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=4, max_length=4, prefix='217', unique=True)),
                ('date_issue', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=15, max_length=20, prefix='TRN', unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(choices=[('failed', 'fallido'), ('completed', 'completado'), ('pending', 'pendiente'), ('processing', 'procesando'), ('requested', 'solicitado'), ('request_send', 'solicitud enviada'), ('request_settled', 'solicitud resuelta'), ('request_processing', 'solicitud en proceso')], default='pending', max_length=100)),
                ('transaction_type', models.CharField(choices=[('trasnfer', 'Transferir'), ('recieved', 'Recivir'), ('withdraw', 'Retirar'), ('refund', 'Reembolso'), ('request', 'Payment Request'), ('none', 'Ninguno')], default='none', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]

# Generated by Django 5.0.4 on 2024-05-05 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_kyc_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='accout_id',
            new_name='account_id',
        ),
    ]
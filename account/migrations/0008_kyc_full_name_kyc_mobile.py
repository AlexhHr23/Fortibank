# Generated by Django 5.0.4 on 2024-05-30 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_kyc_full_name_remove_kyc_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='full_name',
            field=models.CharField(default='Default Name', max_length=1000),
        ),
        migrations.AddField(
            model_name='kyc',
            name='mobile',
            field=models.CharField(default='Default Name', max_length=1000),
        ),
    ]
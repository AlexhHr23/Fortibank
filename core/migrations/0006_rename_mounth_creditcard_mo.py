# Generated by Django 5.0.4 on 2024-05-20 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_creditcard'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creditcard',
            old_name='mounth',
            new_name='mo',
        ),
    ]

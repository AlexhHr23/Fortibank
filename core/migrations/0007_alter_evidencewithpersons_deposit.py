# Generated by Django 5.0.4 on 2024-05-29 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_evidencewithpersons_deposit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidencewithpersons',
            name='deposit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]

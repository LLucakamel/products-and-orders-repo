# Generated by Django 5.1 on 2024-08-08 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='due_date',
            field=models.DateField(),
        ),
    ]

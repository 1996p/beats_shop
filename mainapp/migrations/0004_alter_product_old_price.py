# Generated by Django 3.2.3 on 2021-10-30 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20211030_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Старая цена'),
        ),
    ]
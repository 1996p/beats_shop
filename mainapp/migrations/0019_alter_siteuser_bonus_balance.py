# Generated by Django 4.0.1 on 2022-07-04 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_siteuser_bonus_balance_order_cartproduct_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='bonus_balance',
            field=models.PositiveIntegerField(default=0, verbose_name='Бонусные баллы '),
        ),
    ]

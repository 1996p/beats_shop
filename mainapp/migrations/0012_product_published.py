# Generated by Django 4.0.1 on 2022-02-19 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='published',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата публикации'),
        ),
    ]

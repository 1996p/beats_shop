# Generated by Django 4.0.1 on 2022-02-19 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_product_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='published',
            field=models.DateTimeField(null=True, verbose_name='Дата публикации'),
        ),
    ]
# Generated by Django 4.0.1 on 2022-07-02 17:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_alter_cart_options_alter_cartproduct_options_and_more'),
    ]

    operations = [

        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('status', models.CharField(choices=[('O', 'OPENED'), ('C', 'CLOSED')], default='O', max_length=1, verbose_name='Статус заказа')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.siteuser', verbose_name='Покупатель')),
            ],
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.order'),
        ),
    ]

# Generated by Django 4.2.5 on 2023-10-03 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('sales_network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoleProprietor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='proprietor_name')),
                ('debt_to_supplier', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='debt_to_supplier')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('contact_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='proprietor_contacts', to='sales_network.contactinfo')),
                ('factory_supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proprietor_supplier', to='sales_network.factory', verbose_name='proprietor_supplier')),
                ('products', models.ManyToManyField(related_name='proprietor_products', to='products.product')),
                ('retail_network_supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proprietor_supplier', to='sales_network.retailnetwork', verbose_name='proprietor_supplier')),
            ],
        ),
    ]

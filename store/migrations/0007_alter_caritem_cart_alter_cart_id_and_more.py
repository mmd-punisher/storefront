# Generated by Django 4.2.6 on 2023-11-09 11:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_orderitem_product_alter_product_collection_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caritem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='store.cart'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='caritem',
            unique_together={('cart', 'product')},
        ),
    ]

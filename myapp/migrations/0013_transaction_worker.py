# Generated by Django 5.1.3 on 2024-12-04 17:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_purchasedvoucher'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='myapp.worker', verbose_name='Worker'),
        ),
    ]

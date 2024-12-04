# Generated by Django 5.1.3 on 2024-12-04 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_worker_sub_categories_testimonial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='worker',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]

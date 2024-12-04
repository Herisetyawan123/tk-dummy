# Generated by Django 5.1.3 on 2024-12-03 23:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_jobcategory_alter_user_address_alter_user_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='sub_categories',
            field=models.ManyToManyField(related_name='workers', to='myapp.subjobcategory'),
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.PositiveIntegerField()),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonials', to='myapp.subjobcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testimonials', to='myapp.user')),
            ],
        ),
    ]
# Generated by Django 3.2 on 2021-04-19 08:37

from django.db import migrations, models

import apps.products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.products.models.image_upload_path)),
                ('featured', models.BooleanField(default=False)),
            ],
        ),
    ]

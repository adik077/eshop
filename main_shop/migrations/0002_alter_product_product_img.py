# Generated by Django 3.2.7 on 2021-09-25 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_img',
            field=models.ImageField(blank=True, null=True, upload_to='product_images'),
        ),
    ]

# Generated by Django 4.2.9 on 2024-02-02 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.FileField(upload_to='Photo'),
        ),
    ]

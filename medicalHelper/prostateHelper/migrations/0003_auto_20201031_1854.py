# Generated by Django 3.1.2 on 2020-10-31 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prostateHelper', '0002_auto_20201031_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='pathToOriginal',
        ),
        migrations.AddField(
            model_name='image',
            name='original',
            field=models.ImageField(default=None, upload_to='images/'),
            preserve_default=False,
        ),
    ]

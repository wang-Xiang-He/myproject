# Generated by Django 2.0 on 2020-03-10 11:46

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20200310_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='userprofile/%Y%m%d'),
        ),
    ]

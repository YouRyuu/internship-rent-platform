# Generated by Django 2.1.7 on 2019-03-06 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_platform', '0008_auto_20190305_0438'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='images/')),
            ],
        ),
    ]

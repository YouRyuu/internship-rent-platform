# Generated by Django 2.1.7 on 2019-03-01 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_platform', '0005_auto_20190301_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(null=True),
        ),
    ]

# Generated by Django 3.2 on 2021-05-05 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrasync', '0002_auto_20210505_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawlstate',
            name='crawlid',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='crawlstate',
            name='urlid',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
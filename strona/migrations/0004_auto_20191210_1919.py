# Generated by Django 3.0 on 2019-12-10 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strona', '0003_auto_20191210_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveredpackage',
            name='package_destination',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='deliveredpackage',
            name='package_sizes',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='removedpackage',
            name='package_destination',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='removedpackage',
            name='package_sizes',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='package_destination',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='package_sizes',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
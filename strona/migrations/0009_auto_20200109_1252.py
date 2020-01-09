# Generated by Django 3.0.2 on 2020-01-09 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strona', '0008_auto_20200108_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldchange',
            name='status',
            field=models.CharField(choices=[('NDY', 'Not Deposited Yet'), ('DP', 'Depository'), ('IT', 'In Transit'), ('DE', 'Delivering')], default='NDY', max_length=3),
        ),
        migrations.AddField(
            model_name='packagechange',
            name='status',
            field=models.CharField(choices=[('NDY', 'Not Deposited Yet'), ('DP', 'Depository'), ('IT', 'In Transit'), ('DE', 'Delivering')], default='NDY', max_length=3),
        ),
    ]

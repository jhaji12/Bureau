# Generated by Django 5.0.4 on 2024-04-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='dateTimeTransaction',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='originalDataElement',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

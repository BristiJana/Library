# Generated by Django 5.0.6 on 2024-05-25 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='borrower',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

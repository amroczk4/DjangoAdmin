# Generated by Django 4.1.1 on 2022-10-20 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodrle', '0006_alter_dishes_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishes',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

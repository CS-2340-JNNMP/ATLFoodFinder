# Generated by Django 5.1.1 on 2024-10-01 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]

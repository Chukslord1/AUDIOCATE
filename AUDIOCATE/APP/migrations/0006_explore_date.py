# Generated by Django 2.2.4 on 2020-12-14 00:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0005_explore'),
    ]

    operations = [
        migrations.AddField(
            model_name='explore',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

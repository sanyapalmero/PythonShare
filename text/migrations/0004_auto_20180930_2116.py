# Generated by Django 2.1.1 on 2018-09-30 16:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0003_text_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 3.2.25 on 2025-03-09 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest_hub_app', '0002_auto_20250309_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='latitude',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='program',
            name='longitude',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='program',
            name='stage_no',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-17 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymap', '0004_alter_schools_level_alter_schools_sponsor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schools',
            name='stage_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='schools',
            name='stage_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
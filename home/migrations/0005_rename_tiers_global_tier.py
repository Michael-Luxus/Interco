# Generated by Django 5.1.1 on 2024-09-16 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_global_remove_tier_value_tier_societe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='global',
            old_name='tiers',
            new_name='tier',
        ),
    ]

# Generated by Django 3.2.12 on 2022-12-28 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0019_auto_20221226_0300'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductCategory',
            new_name='ProductCampaign',
        ),
        migrations.RenameField(
            model_name='recipient',
            old_name='current_offering',
            new_name='current_campaign',
        ),
    ]

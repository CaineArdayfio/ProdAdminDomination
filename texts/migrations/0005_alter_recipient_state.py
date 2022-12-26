# Generated by Django 3.2.12 on 2022-12-25 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0004_auto_20221225_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='state',
            field=models.CharField(choices=[('UnknownPreference', 'UnknownPreference'), ('AffirmativePurchase', 'AffirmativePurchase'), ('NegativePurchase', 'NegativePurchase'), ('MetadataExists', 'MetadataExists'), ('NoneorIncorrectMetadata', 'NoneorIncorrectMetadata'), ('MetadataExists', 'MetadataExists'), ('CorrectMetadata', 'CorrectMetadata'), ('NoPaymentData', 'NoPaymentData'), ('PaymentRequested', 'PaymentRequested'), ('InvalidPaymentDetails', 'InvalidPaymentDetails')], default='UnknownPreference', max_length=30),
        ),
    ]

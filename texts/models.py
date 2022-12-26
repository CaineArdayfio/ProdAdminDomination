from django.db import models
from django.urls import reverse
from model_utils import Choices
from decimal import Decimal


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    GENDER = Choices("Male", "Female", "Unisex")
    gender = models.CharField(
        max_length=30, choices=GENDER, default=GENDER.Male)

    TYPE = Choices("Tops", "Bottoms", "Shoes")
    type = models.CharField(
        max_length=30, choices=TYPE, default=TYPE.Tops)

    def save(self, *args, **kwargs):
        # Full clean throws an error if the chosen state is not
        self.full_clean()
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Recipient(models.Model):
    phone = models.CharField(max_length=100, unique=True, primary_key=True)
    STATE = Choices('InvalidState', 'UnknownPreference', 'AffirmativePurchase', 'NegativePurchase', 'MetadataExists', 'NoneOrIncorrectMetadata',
                    'MetadataExists', 'CorrectMetadata', 'NoPaymentData', 'PaymentRequested', 'InvalidPaymentDetails', 'PaymentAndMetadataCorrect', 'Terminated')
    state = models.CharField(
        max_length=30, choices=STATE, default=STATE.UnknownPreference)
    current_offering = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, blank=True)

    # Clothing
    SIZES = Choices('XS', 'S', 'M', 'L', 'XL')
    # Shoes
    SHOES = Choices('8', '9', '10', '11', '12')
    bottom_sizes = models.CharField(
        max_length=30, choices=SIZES, blank=True)
    top_sizes = models.CharField(
        max_length=30, choices=SIZES, blank=True)

    def save(self, *args, **kwargs):
        # Full clean throws an error if the chosen state is not
        self.full_clean()
        super(Recipient, self).save(*args, **kwargs)


class Product(models.Model):
    product_id = models.CharField(
        max_length=100, unique=True, primary_key=True)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE)
    # Store numbers up to 9,999.99 with a resolution of two decimal places
    price = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal(0.00))

    size = models.CharField(
        max_length=30, default="M")

    def save(self, *args, **kwargs):
        # Full clean throws an error if the chosen state is not
        self.full_clean()
        super(Product, self).save(*args, **kwargs)

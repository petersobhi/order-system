from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum

from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.models.managers import money_manager

User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def category_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/categories/<slug>.<ext>
    slug = instance.slug
    basename, file_extension = filename.split(".")
    new_filename = "%s.%s" % (slug, file_extension)
    return 'categories/{0}'.format(new_filename)


class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to=category_image_path, blank=True)


def product_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/products/<slug>.<ext>
    basename, file_extension = filename.split(".")
    new_filename = "%s.%s" % (instance.created, file_extension)
    return 'products/{0}'.format(new_filename)


class ProductManager(models.Manager):
    def with_converted_price(self, currency):
        """
        Return product list with localized prices based on user currency
        :param currency
        :return: product list
        """
        products = self.all()
        for product in products:
            product.converted_price = convert_money(product.price, currency)
        return products


class Product(TimeStampedModel):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = money_manager(ProductManager())


class OrderManager(models.Manager):
    def revenue(self):
        result = [
            {'amount': data['total_amount__sum'], 'currency': data['total_amount_currency']} for data in
            self.values('total_amount_currency').annotate(Sum('total_amount'))
        ]
        return result


class Order(TimeStampedModel):
    class Statuses(models.TextChoices):
        PENDING = 'pn', 'Pending'
        FINISHED = 'fn', 'Finished'  # Finished by user
        DELIVERED = 'dl', 'Delivered'

    class PaymentMethods(models.TextChoices):
        COD = 'cod', 'Cash on delivery'

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Statuses.choices, default=Statuses.PENDING)
    payment_method = models.CharField(max_length=3, choices=PaymentMethods.choices, default=PaymentMethods.COD)
    total_amount = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR', default=0)

    objects = money_manager(OrderManager())


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR')
    quantity = models.IntegerField(default=1)

    @property
    def total_amount(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super(OrderItem, self).save(*args, **kwargs)

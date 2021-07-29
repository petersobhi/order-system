import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class ExchangeBackendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'exchange.ExchangeBackend'

    name = factory.Faker('user_name')
    base_currency = factory.Faker('currency_code')


class RateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'exchange.Rate'

    currency = factory.Faker('currency_code')
    backend = factory.SubFactory(ExchangeBackendFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Category'


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Product'

    price = 5
    price_currency = 'EUR'
    seller = factory.SubFactory(UserFactory)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.Order'

    buyer = factory.SubFactory(UserFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.OrderItem'

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)

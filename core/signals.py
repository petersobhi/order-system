from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import OrderItem


@receiver(post_save, sender=OrderItem)
def update_order_total_amount(sender, instance, created, **kwargs):
    instance.order.total_amount += instance.total_amount
    instance.order.save()

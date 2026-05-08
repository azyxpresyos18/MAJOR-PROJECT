from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def auto_assign_department(sender, instance, created, **kwargs):
    """
    When a new product is saved without a department,
    auto-assign it to the first active department of its client.
    """
    if created and instance.department is None and instance.client:
        department = (
            instance.client.departments
            .filter(is_active=True)
            .order_by('created_at')
            .first()
        )
        if department:
            Product.objects.filter(pk=instance.pk).update(department=department)
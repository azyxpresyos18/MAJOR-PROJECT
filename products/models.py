from django.db import models


class ProductCategory(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Product categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    PENDING  = 'pending'
    ACTIVE   = 'active'
    INACTIVE = 'inactive'

    STATUS_CHOICES = [
        (PENDING,  'Pending'),
        (ACTIVE,   'Active'),
        (INACTIVE, 'Inactive'),
    ]

    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='products/', null=True, blank=True)
    category    = models.ForeignKey(
        ProductCategory,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='products'
    )
    client      = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='products'
    )
    department  = models.ForeignKey(
        'departments.Department',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='products'
    )
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['client', 'name']

    def __str__(self):
        return f'{self.name} — {self.client}'
    
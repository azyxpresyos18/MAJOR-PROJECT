from django.db import models


class Department(models.Model):
    SALES        = 'sales'
    MARKETING    = 'marketing'
    LOGISTICS    = 'logistics'
    CREATIVE     = 'creative'
    OPERATIONS   = 'operations'

    TYPE_CHOICES = [
        (SALES,      'Sales'),
        (MARKETING,  'Marketing'),
        (LOGISTICS,  'Logistics'),
        (CREATIVE,   'Creative'),
        (OPERATIONS, 'Operations'),
    ]

    name        = models.CharField(max_length=100, unique=True)
    dept_type   = models.CharField(max_length=30, choices=TYPE_CHOICES, default=OPERATIONS)
    description = models.TextField(blank=True)
    client      = models.ForeignKey(
        'clients.Client',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='departments'
    )
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
from django.db import models


class Mall(models.Model):
    name    = models.CharField(max_length=200, unique=True)
    address = models.TextField()
    city    = models.CharField(max_length=100, default='Cebu City')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Schedule(models.Model):
    PENDING   = 'pending'
    CONFIRMED = 'confirmed'
    ONGOING   = 'ongoing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING,   'Pending'),
        (CONFIRMED, 'Confirmed'),
        (ONGOING,   'Ongoing'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    title       = models.CharField(max_length=255)
    client      = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    products    = models.ManyToManyField(
        'products.Product',
        related_name='schedules',
        blank=True
    )
    department  = models.ForeignKey(
        'departments.Department',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='schedules'
    )
    mall        = models.ForeignKey(
        Mall,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    assigned_to = models.ForeignKey(
        'accounts.Employee',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='schedules'
    )
    start_datetime = models.DateTimeField()
    end_datetime   = models.DateTimeField()
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return f'{self.title} @ {self.mall} ({self.start_datetime:%Y-%m-%d})'

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_datetime and self.start_datetime:
            if self.end_datetime <= self.start_datetime:
                raise ValidationError('End time must be after start time.')
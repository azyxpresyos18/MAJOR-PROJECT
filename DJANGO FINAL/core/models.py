from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.client.name} – {self.name}"

    class Meta:
        ordering = ['client__name', 'name']


class Location(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    floor_area = models.CharField(max_length=50, blank=True)
    open_hours = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} – {self.city}"

    class Meta:
        ordering = ['name']


class Schedule(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('ongoing',   'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client          = models.ForeignKey(Client,     on_delete=models.CASCADE, related_name='schedules')
    product         = models.ForeignKey(Product,    on_delete=models.CASCADE, related_name='schedules')
    department      = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='schedules')
    location        = models.ForeignKey(Location,   on_delete=models.CASCADE, related_name='schedules')
    scheduled_date  = models.DateField()
    scheduled_time  = models.TimeField()
    quantity        = models.PositiveIntegerField(default=1)
    assigned_to     = models.CharField(max_length=150)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes           = models.TextField(blank=True)
    created_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} @ {self.location.name} – {self.scheduled_date}"

    class Meta:
        ordering = ['scheduled_date', 'scheduled_time']

from django.db import models
from datetime import timedelta, date, datetime
from movies.models import Video

class Package(models.Model):
    DURATION_CHOICES = [
        (30, '30 Days'),
        (90, '90 Days'),
        (365, '1 Year'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    validity_days = models.PositiveIntegerField(choices=DURATION_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_validity_days_display()})"

class Subscription(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='subscriptions')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
       if not self.start_date:
        self.start_date = date.today() 
    
        if not self.package:
            raise ValueError("A valid package must be provided.")
        if not isinstance(self.package.validity_days, int) or self.package.validity_days <= 0:
            raise ValueError("The package's validity_days must be a positive integer.")

        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.package.validity_days)
        super().save(*args, **kwargs)

    def is_active(self):
        return date.today() <= self.end_date

    def __str__(self):
        return f"{self.user.username} - {self.package.name}"


class AccessLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='access_logs')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='access_logs')
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} accessed {self.video.title} on {self.accessed_at}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment by {self.user.username} on {self.payment_date} - {self.status}"
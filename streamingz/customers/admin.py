from django.contrib import admin
from .models import Package, Subscription, Video, AccessLog, Payment
from datetime import timedelta, date

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'validity_days')
    search_fields = ('name',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'start_date', 'end_date', 'is_active')
    list_filter = ('start_date', 'end_date', 'package')
    search_fields = ('user__username', 'package__name')

    def is_active(self, obj):
        return obj.is_active()
    is_active.boolean = True


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'accessed_at')
    list_filter = ('accessed_at',)
    search_fields = ('user__username', 'video__title')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_date', 'transaction_id', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('user__username', 'transaction_id')

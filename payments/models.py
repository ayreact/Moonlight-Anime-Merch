from django.db import models
from products.models import Order
from django.utils import timezone
import secrets
from .paystack  import  Paystack
from django.conf import settings

# Create your models here.
class UserWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    currency = models.CharField(max_length=50, default='NGN')
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.__str__()

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)  # Link payment to order
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.ref} - Amount: {self.amount} - Verified: {self.verified}"

    def save(self, *args, **kwargs):
        # Ensure that the ref field is unique
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            if not Payment.objects.filter(ref=ref).exists():
                self.ref = ref
        super().save(*args, **kwargs)
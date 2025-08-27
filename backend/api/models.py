import os
import uuid
from django.db import models
from django.contrib.auth.hashers import make_password

# -------------------- Role --------------------
class Role(models.Model):
    RoleID = models.AutoField(primary_key=True)
    RoleName = models.CharField(max_length=50)

    def __str__(self):
        return self.RoleName

# -------------------- User --------------------
class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Mobile = models.CharField(max_length=15)
    Salt = models.CharField(max_length=64)
    PasswordHash = models.CharField(max_length=128)
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def id(self):
        return self.UserID

    def set_password(self, raw_password):
        self.Salt = os.urandom(32).hex()
        salted = raw_password + self.Salt
        self.PasswordHash = make_password(salted)

    def __str__(self):
        return self.Email

# -------------------- ServiceRequest --------------------
class ServiceRequest(models.Model):
    RequestID = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    ServiceType = models.CharField(max_length=100)
    Description = models.TextField()
    FeeAmount = models.DecimalField(max_digits=10, decimal_places=2)
    Status = models.CharField(max_length=50)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ServiceType} - {self.Status}"

# -------------------- AuditLog --------------------
class AuditLog(models.Model):
    LogID = models.AutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Action = models.CharField(max_length=255)
    Timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.User.Email} - {self.Action}"

# -------------------- PaymentTransaction --------------------
class PaymentTransaction(models.Model):
    TransactionID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    Request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='payments')
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Currency = models.CharField(max_length=10, default='INR')
    OrderId = models.CharField(max_length=100, unique=True)
    PaymentId = models.CharField(max_length=100, unique=True, null=True, blank=True)
    Signature = models.CharField(max_length=256, null=True, blank=True)
    Status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Success', 'Success'),
            ('Failed', 'Failed'),
            ('Refunded', 'Refunded')
        ],
        default='Pending'
    )
    GatewayResponse = models.JSONField()
    IdempotencyKey = models.CharField(max_length=100, unique=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['PaymentId']),
            models.Index(fields=['IdempotencyKey']),
        ]
        verbose_name = "Payment Transaction"
        verbose_name_plural = "Payment Transactions"

    def __str__(self):
        return f"{self.TransactionID} | {self.Status} | ₹{self.Amount}"

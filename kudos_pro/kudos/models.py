from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')
    remaining_kudos = models.PositiveIntegerField(default=3)
    last_kudo_reset = models.DateTimeField(default=timezone.now)
    
    # Add these to resolve the clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="kudos_user_set",
        related_query_name="kudos_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="kudos_user_set",
        related_query_name="kudos_user",
    )

    def reset_kudos(self):
        if (timezone.now() - self.last_kudo_reset).days >= 7:
            self.remaining_kudos = 3
            self.last_kudo_reset = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.username} ({self.organization})"

class Kudo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kudos_given')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kudos_received')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Kudo from {self.from_user} to {self.to_user}"
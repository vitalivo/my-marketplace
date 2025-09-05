from django.conf import settings
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('provider', 'Самозанятый'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} – {self.get_role_display()}'
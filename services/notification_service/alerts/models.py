from django.conf import settings
from django.db import models


class Alert(models.Model):
    """
    Оповещение, принадлежащее пользователю.

    Пользователь берётся из встроенной модели Django
    (`settings.AUTH_USER_MODEL`). Это гарантирует отсутствие конфликтов
    и даёт возможность позже «привязать» профиль к внешнему сервису,
    не меняя схему базы.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,          # <-- ссылка на стандартного User
        on_delete=models.CASCADE,
        related_name="alerts",
        help_text="Пользователь, которому принадлежит оповещение",
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"

    def __str__(self) -> str:
        return f"{self.title} ({self.user.username})"
    
    
class UserProfile(models.Model):
    """
    Дополнительные данные о пользователе, которые хранятся отдельно
    от встроенной модели Django. Позволяет привязывать внешний сервис
    без переопределения модели пользователя.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    external_auth_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Идентификатор пользователя в стороннем сервисе",
    )

    def __str__(self):
        return f"Profile of {self.user.username}"    
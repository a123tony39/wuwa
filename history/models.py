from django.db import models
from django.contrib.auth.models import User


class EchoHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="echo_histories"
    )

    image = models.ImageField(
        upload_to="history_results/",
        verbose_name="結果圖片",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="建立時間"
    )

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
from django.db import models
from django.contrib.auth.models import User

class TelegramBotToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return f"Token for {self.user.username}"

class TelegramMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    message_body = models.TextField()

    def __str__(self):
        return f"Message from {self.user.username} at {self.date_sent}"


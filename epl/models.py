from django.db import models
from django.utils.translation import ugettext_lazy as _

class ReplyMail(models.Model):
    """Model for general sender : No-reply or webmaster"""
    sendermail = models.EmailField('email')
    def __str__(self):
        return self.sendermail

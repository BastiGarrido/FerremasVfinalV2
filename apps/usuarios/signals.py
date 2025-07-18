
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Cada vez que se cree un User nuevo, genera automáticamente su Token.
    """
    if created:
        Token.objects.create(user=instance)
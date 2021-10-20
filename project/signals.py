from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user, name=user.username, email=user.email)
        profile.save()
        subject = f"Welcome {profile.name} to DevSearch"
        message = "We are glad you are here"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    if user:
        user.delete()


def updateUser(sender, instance, created, **kwargs):
    user = instance.user
    if created == False:
        if user:
            user.username = instance.name
            user.email = instance.email
            user.save()


post_save.connect(create_profile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)

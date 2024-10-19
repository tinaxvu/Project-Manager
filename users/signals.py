from django.contrib.auth.models import Group
from social_django.models import UserSocialAuth
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=UserSocialAuth)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        # Get the user from the UserSocialAuth instance
        user = instance.user

        default_group, _ = Group.objects.get_or_create(name="Common")
        user.groups.add(default_group)
        print("User created")

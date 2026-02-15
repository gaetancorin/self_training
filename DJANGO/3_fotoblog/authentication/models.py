from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    follows = models.ManyToManyField(
        'self',
        limit_choices_to={'role': CREATOR},
        symmetrical=False,
        verbose_name='suit',
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Ajoute le user créer dans un group pour permission
        creator_groups = Group.objects.get(name='creators')
        subscribers_groups = Group.objects.get(name='subscribers')
        if self.role == User.CREATOR:
            creator_groups.user_set.add(self)
        elif self.role == User.SUBSCRIBER:
            subscribers_groups.user_set.add(self)

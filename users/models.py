from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.models import Professors, Students

class User(AbstractUser):
    professor = models.ForeignKey(
        Professors,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
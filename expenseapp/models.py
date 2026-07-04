from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    amount = models.FloatField(default=0)


class Expense(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    amount = models.FloatField()

    category = models.CharField(max_length=50)

    date = models.DateField()

    def __str__(self):
        return self.title
    
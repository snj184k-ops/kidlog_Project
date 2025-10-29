from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Child(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    photo = models.ImageField(upload_to="child_photos/", blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def age_years_months(self):
        today = date.today()
        years = today.year - self.birth_date.year
        months = today.month - self.birth_date.month

        if months < 0 or (months == 0 and today.day < self.birth_date.day):
            years -= 1
            months += 12

        if today.day < self.birth_date.day:
            months -= 1
            if months < 0:
                years -= 1
                months += 12

        return years, months

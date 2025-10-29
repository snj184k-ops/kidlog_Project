from django.db import models
from child_selection.models import Child


class MilkRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    time = models.DateTimeField()
    amount = models.IntegerField()
    note = models.TextField(blank=True, null=True)


class SleepRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    note = models.TextField(blank=True, null=True)

    @property
    def duration_hours(self):
        return (self.end_time - self.start_time).total_seconds() / 3600


class PoopRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    time = models.DateTimeField()
    note = models.TextField(blank=True, null=True)


class PeeRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    time = models.DateTimeField()
    note = models.TextField(blank=True, null=True)


class TemperatureRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    time = models.DateTimeField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    note = models.TextField(blank=True, null=True)


class FoodRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    time = models.DateTimeField()
    menu = models.CharField(max_length=255)
    amount = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)


class HtmtRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    date = models.DateField()

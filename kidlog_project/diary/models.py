from django.db import models
from child_selection.models import Child


class DiaryRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    time = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    summary = models.TextField(null=True)

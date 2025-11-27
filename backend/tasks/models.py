
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    importance = models.IntegerField(default=5)
    estimated_hours = models.FloatField(default=1)
    due_date = models.DateField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

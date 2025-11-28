
from django.db import models

class AnalyzedTask(models.Model):
    title = models.CharField(max_length=200)
    importance = models.IntegerField()
    estimated_hours = models.FloatField()
    due_date = models.DateField(null=True, blank=True)
    score = models.FloatField()
    priority = models.CharField(max_length=50)

    def __str__(self):
        return self.title




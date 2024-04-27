from django.db import models

# Create your models here.
class JobApplicant(models.Model):
    major = models.CharField(max_length=100) 
    degree = models.CharField(max_length=20)

    workHistoryCount = models.PositiveIntegerField()
    managedHowMany = models.PositiveIntegerField()
    yearsOfExp = models.PositiveIntegerField()

    currentlyEmployed = models.CharField(max_length=3)
    managedOthers = models.CharField(max_length=3)
    workHistory = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
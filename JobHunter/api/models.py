from django.db import models

# Create your models here.
class JobApplicant(models.Model):
    NONE = 'None'
    HIGH_SCHOOL = 'High School'
    VOCATIONAL = "Vocational"
    ASSOCIATES = "Associate's"
    BACHELORS = "Bachelor's"
    MASTERS = "Master's"
    PHD = "PhD"

    DEGREE_CHOICES = (
        (NONE, 'None'),
        (HIGH_SCHOOL, 'High School'),
        (VOCATIONAL, 'Vocational'),
        (ASSOCIATES, "Associate's"),
        (BACHELORS, "Bachelor's"),
        (MASTERS, "Master's"),
        (PHD, "PhD"),
    )

    YES = 'Yes'
    NO = 'No'

    CURRENTLY_EMPLOYED_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No'),
    )

    degree_type = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    work_history_count = models.PositiveIntegerField()
    total_years_experience = models.FloatField()
    currently_employed = models.CharField(max_length=3, choices=CURRENTLY_EMPLOYED_CHOICES)
    managed_others = models.CharField(max_length=3, choices=CURRENTLY_EMPLOYED_CHOICES)
    managed_how_many = models.PositiveIntegerField()
    workexp = models.JSONField(default=list)

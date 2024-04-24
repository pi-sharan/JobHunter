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

    major = models.CharField(max_length=100) 
    degree_type = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    work_history_count = models.PositiveIntegerField()
    total_years_experience = models.FloatField()
    currently_employed = models.CharField(max_length=3, choices=CURRENTLY_EMPLOYED_CHOICES)
    managed_others = models.CharField(max_length=3, choices=CURRENTLY_EMPLOYED_CHOICES)
    managed_how_many = models.PositiveIntegerField()
    # TODO Confirm if this a list or a single value
    past_work_ex = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
from django.db import models
from django.conf import settings

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    DEGREE_TYPE_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    university = models.CharField(max_length=100)
    academic_year = models.IntegerField()
    degree_type = models.CharField(max_length=20, choices=DEGREE_TYPE_CHOICES)
    nickname = models.CharField(max_length=30, unique=True)
    languages = models.JSONField(default=list)  # ["English", "Korean"] 이런 식 저장
    interests = models.JSONField(default=list)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.nickname

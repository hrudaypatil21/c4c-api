from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
import re
import os


class CustomUser(AbstractUser):
    """Base user model extended for our platform"""
    USER_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('ngo', 'NGO'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()
        super().save(*args, **kwargs)
    
    def generate_username(self):
        """Generate username from email with random suffix if needed"""
        base = self.email.split('@')[0]
        clean = re.sub(r'[^a-z0-9]', '', base.lower())
        if CustomUser.objects.filter(username=clean).exists():
            from random import randint
            clean = f"{clean}_{randint(100, 999)}"
        return clean

class IndividualProfile (models.Model):
    """Extended profile for individual users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    skills = models.JSONField(default=list)
    interests = models.JSONField(default=list)
    availability = models.CharField(
        max_length=20,
        choices=[
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('occasionally', 'Occasionally'),
            ('one-time', 'One-time projects only')
        ],
        default='occasionally'
    )
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='user_resumes/', blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

def ngo_verification_path(instance, filename):
    """File upload path for NGO verification docs"""
    return f'ngo_verifications/{instance.user.id}/{filename}'

class NGOProfile(models.Model):
    """Extended profile for NGOs"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='ngo_profile')
    org_name = models.CharField(max_length=255)
    reg_number = models.CharField(max_length=100, unique=True)
    org_phone = models.CharField(max_length=20)
    org_address = models.TextField()
    org_mission = models.TextField()
    org_website = models.URLField(blank=True)
    vol_needs = models.JSONField(default=list)  # Store needed volunteer skills
    verification_docs = models.FileField(upload_to=ngo_verification_path)
    is_verified = models.BooleanField(default=False)
    founded_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.org_name
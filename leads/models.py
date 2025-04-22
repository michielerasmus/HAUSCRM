from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, User

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):

    SOURCE_CHOICES = (
        ('Agent Referral', 'Agent Referral'),
        ('Cold Calling', 'Cold Calling'),
        ('Flyer', 'Flyer'),
        ('Hot List', 'Hot List'),
        ('Marketing Day', 'Marketing Day'),
        ('Newsletter', 'Newsletter'),
        ('Other', 'Other'),
        ('Outside Referral', 'Outside Referral'),
        ('Private Property', 'Private Property'),
        ('Property 24', 'Property 24'),
        ('Social Media', 'Social Media'),
        ('Walk In', 'Walk In'),
        ('Website', 'Website'),
    )

    STATUS_CHOICES = (
        ('New Lead', 'New Lead'),
        ('Follow Up', 'Follow Up'),
        ('Schedule Appointment', 'Schedule Appointment'),
        ('Lead Won', 'Lead Won'),
        ('Lead Lost', 'Lead Lost'),
    )

    name = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    detail = models.TextField(blank=True, null=True)
    contacted = models.BooleanField(default=False)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return f"Lead ID: {self.id} (No Name)"

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
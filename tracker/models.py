from django.db import models
from leads.models import Agent

class Tracker(models.Model):
    month = models.CharField(max_length=100)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    calls_made = models.IntegerField(null=True, blank=True)
    appointments_set = models.IntegerField(null=True, blank=True)
    listings_secured = models.IntegerField(null=True, blank=True)
    showings_concluded = models.IntegerField(null=True, blank=True)
    deals_closed = models.IntegerField(null=True, blank=True)
    follow_ups = models.IntegerField(null=True, blank=True)
    social_media_posts = models.IntegerField(null=True, blank=True)
    database_growth = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this field

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Tracker for {self.month} by {self.agent}" #It is better to return a more descriptive string.
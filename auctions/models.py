from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORY_CHOICES = [('No category', 'No category'), ('Toys', 'Toys'), ('Home', 'Home'), ('Garden', 'Garden'), ('Books', 'Books')]
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
            related_name='my_listings')
    posted_date = models.DateTimeField(default=timezone.now, blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=30000)
    starting_bid = models.FloatField()
    current_price = models.FloatField()
    imageURL = models.CharField(max_length=3000, blank=True) 
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='No category') 
    is_active = models.BooleanField(default=True)
    watched_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="watching")

    def save(self, *args, **kwargs):
        if self.current_price is None:
            self.current_price = self.starting_bid
        super(Listing, self).save(*args, **kwargs)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = 'l_bids')
    bid_date = models.DateTimeField(default=timezone.now, blank=True)
    amount = models.FloatField()
    bid_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
            related_name = 'u_bids')

class Comment(models.Model):
    listing  = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = 'comments')
    comment_datetime = models.DateTimeField(default=timezone.now, blank=True)
    text = models.CharField(max_length=30000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
            related_name='my_comments')

    

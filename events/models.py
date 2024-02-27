from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Venue(models.Model):
    name = models.CharField('Event Name', max_length=120)
    address = models.CharField('Address', max_length=300)
    zip_code = models.CharField('Zip Code', max_length=10)
    phone = models.CharField('Contact Phone', blank=True, max_length=25)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, default=1)
    venue_image = models.ImageField(blank=True, null=True, upload_to='images/') 
    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    #venue = models.CharField(max_length=120)
    manager = models.ForeignKey(User, related_name='manager', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(User, related_name='attendee', blank=True)
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name

    @property
    def days_till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        days_till_stripped = str(days_till).strip(',')[0]
        
        if self.event_date.date() < today:
            return 'Event already passed'
        else: 
            return f'{days_till_stripped} Days'



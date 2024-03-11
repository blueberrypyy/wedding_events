from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Event, Venue, MyClubUser
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
from django.contrib import messages
import csv

#import pdf stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import pagination stuff
from django.core.paginator import Paginator

from django.contrib.auth.models import User

# Geneate PDF of venues
def venue_pdf(request):
    # Create bytestream bffer
    buf = io.BytesIO()
    # Create canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create text object 
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Add some lines of text
    lines = ["this is line 1\n",
            "this is line2\n",
            "this is line3\n\n",
            "I am awesome\n"]

    # Deignate the model 
    venues = Venue.objects.all()

    # Create a blank list 
    lines =[]

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(' ')

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # return something
    return FileResponse(buf, as_attachment=True, filename='venues.pdf')


# Generate csv file
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the model 
    venues = Venue.objects.all()

    # Add column headings for csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Website', 'Email Address'])

    # Loop thru and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

    return response


# Generate text file
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    # Designate the model
    venues = Venue.objects.all()

    # Create blank list
    lines = []
    # Loop thru and output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n')
    #lines = ["this is line 1\n",
    #        "this is line2\n",
    #        "this is line3\n\n",
    #        "I am awesome\n"]

    # Write to text file
    response.writelines(lines)
    return response 

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')

    return render(request, 'events/update_venue.html', {'venue': venue, 'form': form, })

def venue_events(request, venue_id):
    events = Event.venue.all().where(id=pk)
    return render(request, 'events/venue_events.html', {'events': events})


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues, })
    else:
        return render(request, 'events/search_venues.html', {})

def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')

    # Set up pagination
    p = Paginator(Venue.objects.all(), 4)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = 'a' * venues.paginator.num_pages

    return render(request, 'events/venues.html', {'venue_list': venue_list, 'venues': venues, 'nums': nums})

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    # take id (num) and convert it to owner name
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {'venue': venue, 'venue_owner': venue_owner})

def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        # Save user id to the event in backend whenever they add an event 
        if form.is_valid:
            venue = form.save(commit=False)
            venue.owner = request.user.id # Logged in user
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True') 

    else: 
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venues')

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    # make sure only event manager can delete without using url
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('events_list')
    else:
        messages.success(request, 'You must be the event manager to delete an event.')
        return redirect('events_list')

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events_list')

    return render(request, 'events/update_event.html', {'event': event, 'form': form, })

def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        my_events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html', {'my_events': my_events})
    else: 
        messages.success(request, 'You are not authorized to view this page.')
        return redirect('home')

def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)
        return render(request, 'events/search_events.html', {'searched': searched, 'events': events, })
    else:
        return render(request, 'events/search_events.html', {})

def approve_events(request):
    events = Event.objects.all().order_by('-event_date')
    venues = Venue.objects.all()
    event_count = events.count()
    venue_count = Venue.objects.all().count()
    user_count = MyClubUser.objects.all().count() 
    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')

            # Set all approved to false
            events.update(approved=False)

            # Update database (hack)
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request, 'Event approval updated successfully.')
            return redirect('approve_events')
        else:
            return render(request, 'events/event_approval.html', {'events': events, 'venues': venues, 'event_count': event_count, 'venue_count': venue_count, 'user_count': user_count})
    else:
        messages.success(request, 'You are not authorized to view this page')
        return redirect('home')

def add_event(request):
    submitted = False
    current_user = request.user
    if request.method == 'POST':
        # Render different form if user is admin or not 
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user # Logged in user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user # Logged in user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')

    else: 
        # Just going to the page not submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})

def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    return render(request, 'events/events_list.html', 
            {'event_list': event_list})


def homePageView(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = '' 
    month = month.title()

    # Convert month to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # Create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Get current year 
    now = datetime.now()
    current_year = now.year

    #Query the events model for the dates
    events_list = Event.objects.filter(event_date__year=year, event_date__month=month_number)

    return render(request, 'events/home.html', {
            'name': name,
            'year': year,
            'month': month,
            'month_number': month_number,
            'cal': cal,
            'current_year': current_year,
            'events_list': events_list
            })

def landingPageView(request):
    return render(request, 'events/landing_page_main.html', {})

def test1(request):
    return render(request, 'events/test_typing.html', {})

def test2(request):
    return render(request, 'events/test_waves.html', {})





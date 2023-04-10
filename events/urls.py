from django.urls import path
from . import views

urlpatterns = [
        path('portfolio/', views.landingPageView, name='landing_page'),
        path('test1/', views.test1, name='test1'),
        path('test2/', views.test2, name='test2'),


        path('', views.homePageView, name='home'),
        path('<int:year>/<str:month>/', views.homePageView, name='home'),
        path('events/', views.all_events, name='events_list'),
        path('add_venue/', views.add_venue, name='add_venue'),
        path('list_venues/', views.list_venues, name='list_venues'),
        path('show_venue/<venue_id>/', views.show_venue, name='show_venue'),
        path('search_venues/', views.search_venues, name='search_venues'),
        path('update_venue/<venue_id>/', views.update_venue, name='update_venue'),
        path('add_event/', views.add_event, name='add_event'),
        path('update_event/<event_id>', views.update_event, name='update_event'),
        path('delete_event/<event_id>', views.delete_event, name='delete_event'),
        path('delete_venue/<venue_id>', views.delete_venue, name='delete_venue'),
        path('venue_text/', views.venue_text, name='venue_text'),
        path('venue_csv/', views.venue_csv, name='venue_csv'),
        path('venue_pdf/', views.venue_pdf, name='venue_pdf'),
        path('my_events', views.my_events, name='my_events'),
        path('search_events', views.search_events, name='search_events')

        ]

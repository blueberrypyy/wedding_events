from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
]

# Config admin title
admin.site.site_header = 'My Wedding Planner Admin'
admin.site.site_title = 'My Wedding Planner'
admin.site.index_title = 'Welcome to your wedding admin portal'

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("add_venue", views.add_venue, name="addVenue"),
    path('venue/', views.venue, name='venue'),
    path('contact/', views.contact, name='contact'),
    path('venues/', views.venue_list, name='venue-list'),
    path('visit_request/', views.visit_request, name='visit-request'),
    path('table_booking/', views.table_booking, name='table-booking'),
        path('login/', views.user_login, name='user-login'),
    path('register/', views.user_register, name='user-register'), 
       path('single-venue-detail.html', views.venue_detail, name='venue-detail'),
        path('Booking.html', views.booking, name='booking'),
        path('contact.html', views.contact, name='contact'),

]
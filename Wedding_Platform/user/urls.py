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
    path('visit_request_view/', views.visit_request_view, name='visit_request_view'),
    path('table_booking/', views.table_booking, name='table-booking'),
    path('login/', views.user_login, name='user-login'),
    path('register/', views.user_register, name='user-register'), 
    path('venue/<int:venue_id>/', views.venue_detail, name='venue-detail'),
    path('venue/<int:venue_id>/booking/', views.booking, name='booking'),
    path('contact.html', views.contact, name='contact'),
    path('update-visit-status/<int:visit_id>/', views.update_visit_status, name='update_visit_status'),
    path('update-venue-status/<int:venue_id>/', views.update_venue_status, name='update_venue_status'),
    path('update-booking-status/', views.update_booking_status, name='update-booking-status'),  

]
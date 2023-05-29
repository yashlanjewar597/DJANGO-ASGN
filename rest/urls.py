from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView


urlpatterns = [
    path('v1/calendar/init/', GoogleCalendarInitView.as_view(), name='google_permission'),
    path('v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='google_redirect')
]
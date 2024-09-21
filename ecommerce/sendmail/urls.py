from django.urls import path

from .views import confirmation_view, sendmail_view


app_name = "contact"

urlpatterns = [
    path("sendmail/",sendmail_view,name="sendmail"),
    path("confirmation/",confirmation_view,name="confirmation")
]

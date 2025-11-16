from django.urls import path
from . import views

app_name = "trades"

urlpatterns = [
    path("upload/", views.upload_trades, name="upload_trades"),
    path("dashboard/", views.dashboard, name="dashboard"),
]

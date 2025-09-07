from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/", views.add_habit, name="add_habit"),
    path("habit/<int:habit_id>/", views.habit_detail, name="habit_detail"),
    path("habit/<int:habit_id>/data/", views.habit_data, name="habit_data"),
    path("habit/<int:habit_id>/calendar/", views.habit_calendar_data, name="habit_calendar_data"),
    path("signup/", views.signup, name="signup"),
]

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Habit, HabitRecord

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, "habits/dashboard.html", {"habits": habits})

@login_required
def add_habit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Habit.objects.create(name=name, user=request.user)
        return redirect("dashboard")
    return render(request, "habits/add_habit.html")

@login_required
def habit_detail(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    if request.method == "POST":
        today = timezone.now().date()
        success = request.POST.get("success") == "true"
        HabitRecord.objects.update_or_create(
            habit=habit, date=today, defaults={"success": success}
        )
        return redirect("habit_detail", habit_id=habit.id)

    records = habit.records.order_by("-date")
    return render(request, "habits/habit_detail.html", {
        "habit": habit,
        "records": records,
        "current_streak": habit.current_streak(),
        "longest_streak": habit.longest_streak()
    })

@login_required
def habit_data(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    records = habit.records.order_by("date")
    data = [{"date": r.date.strftime("%Y-%m-%d"), "success": r.success} for r in records]
    return JsonResponse(data, safe=False)

@login_required
def habit_calendar_data(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    records = habit.records.all()
    events = []
    for r in records:
        events.append({
            "title": "✅" if r.success else "❌",
            "start": r.date.strftime("%Y-%m-%d"),
            "color": "#22c55e" if r.success else "#ef4444"
        })
    return JsonResponse(events, safe=False)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

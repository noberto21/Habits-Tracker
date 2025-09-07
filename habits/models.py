from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def current_streak(self):
        records = self.records.order_by('-date')
        streak = 0
        today = timezone.now().date()
        for record in records:
            if record.success and (today - record.date).days <= streak:
                streak += 1
            else:
                break
        return streak

    def longest_streak(self):
        records = self.records.order_by('date')
        max_streak = streak = 0
        prev_date = None
        for record in records:
            if record.success:
                if prev_date and (record.date - prev_date).days == 1:
                    streak += 1
                else:
                    streak = 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
            prev_date = record.date
        return max_streak

    def __str__(self):
        return self.name

class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="records")
    date = models.DateField()
    success = models.BooleanField(default=True)

    class Meta:
        unique_together = ("habit", "date")

    def __str__(self):
        return f"{self.habit.name} - {self.date} - {'✅' if self.success else '❌'}"

from datetime import date

from django.db import models
from django.contrib.postgres.fields import IntegerRangeField


class Program(models.Model):
    title = models.CharField(max_length=255)
    amount_range = IntegerRangeField()
    age_range = IntegerRangeField()

    def __str__(self):
        return self.title


def get_birthday_from_pn(personal_number):
    from datetime import datetime
    return datetime.strptime(personal_number[:6], '%y%m%d')


class User(models.Model):
    personal_number = models.CharField(max_length=12, primary_key=True)
    born_at = models.DateField()

    def save(self, *args, **kwargs):
        self.born_at = get_birthday_from_pn(self.personal_number)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.personal_number

    @property
    def age(self):
        return (date.today()-self.born_at).days//365


class Application(models.Model):
    program = models.ForeignKey('Program', on_delete=models.PROTECT, related_name='applications')
    applied_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='applications')
    amount = models.PositiveIntegerField()

    class Status(models.TextChoices):
        confirmed = 'confirmed', 'Confirmed'
        rejected = 'rejected', 'Rejected'
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.confirmed)
    class Reason(models.IntegerChoices):
        amount_not_in_range = 1, 'Заявка не подходит по сумме'
        age_not_in_range = 2, 'Заемщик не подходит по возрасту'
        user_is_ie = 3, 'иин является ИП'
        user_is_blacklisted = 4, 'Заемщик в черном списке'

    rejection_reason = models.IntegerField(choices=Reason.choices, blank=True, null=True)

    def __str__(self):
        return self.program



class BlackList(models.Model):
    personal_number = models.CharField(max_length=12)

    def __str__(self):
        return self.personal_number


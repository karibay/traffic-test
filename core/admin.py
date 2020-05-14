from django.contrib import admin
from .models import Program, BlackList, User, Application


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    pass


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass

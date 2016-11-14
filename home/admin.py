from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Church, Volunteer, Min_Category, Min_Group, Help
# Register your models here.

# class VolunteerInline(admin.StackedInline):
#     model = Volunteer
#     can_delete = False
#     verbose_name_plural = 'volunteers'
#
# class ChurchInline(admin.StackedInline):
#     model = Church
#     can_delete = False
#     verbose_name_plural = 'churches'
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (VolunteerInline, ChurchInline, )
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Church)
admin.site.register(Volunteer)
admin.site.register(Min_Group)
admin.site.register(Min_Category)
admin.site.register(Help)
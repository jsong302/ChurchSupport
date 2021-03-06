from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Church, Volunteer, Min_Category, Min_Group, Help, Help_Request, Interest, Zipcode, Location_Area
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

def getRequests(obj):
    help = Help.objects.filter(church=obj).extra(order_by=['category__name'])
    res = ""
    for h in help:
        res = res + " \n" + h.category.group.name + ": " + h.category.name
    return ("%s" % (res))
getRequests.short_description = 'Requests'

class ChurchAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'approval', getRequests)

admin.site.register(Church, ChurchAdmin)
admin.site.register(Volunteer)
admin.site.register(Min_Group)
admin.site.register(Min_Category)
admin.site.register(Help)
admin.site.register(Help_Request)
admin.site.register(Interest)
admin.site.register(Zipcode)
admin.site.register(Location_Area)
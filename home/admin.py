from django.contrib import admin
from .models import Church, Ministry, Volunteer, Denomination
# Register your models here.


admin.site.register(Church)
admin.site.register(Ministry)
admin.site.register(Volunteer)
admin.site.register(Denomination)
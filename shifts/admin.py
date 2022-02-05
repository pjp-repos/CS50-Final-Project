from shifts.models import Shift
from django.contrib import admin

from .models import Employee,Shift,Slice,Stamp,Schedule

# Register your models here.

admin.site.register(Employee)
admin.site.register(Stamp)
admin.site.register(Shift)
admin.site.register(Slice)
admin.site.register(Schedule)



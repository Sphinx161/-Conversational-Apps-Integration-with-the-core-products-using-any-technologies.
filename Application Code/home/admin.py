from django.contrib import admin

# Register your models here.
from .models import Managers,Employees
# Register your models here.
#
admin.site.register(Managers)
admin.site.register(Employees)

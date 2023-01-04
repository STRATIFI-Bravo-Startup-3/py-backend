from django.contrib import admin
from .models import User, Influencer, Brand, Employee
# Register your models here.

admin.site.register(User)
admin.site.register(Influencer)
admin.site.register(Brand)
admin.site.register(Employee)
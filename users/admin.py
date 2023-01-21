from django.contrib import admin
from .models import User, Influencer, Brand, Employee, Language, Niche
# Register your models here.

admin.site.register(User)
admin.site.register(Influencer)
admin.site.register(Brand)
admin.site.register(Language)
admin.site.register(Niche)
admin.site.register(Employee)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    BrandProfile,
    Brand,
    InfluencerProfile,
    Influencer,
    Niche,
    AgeBracket,
    Platform,
    Language,
    Gender,
    InfluencerType,
    CompanySize,
    InfluencerPool,
    Campaign,
    Job,
)


class BrandProfileInline(admin.StackedInline):
    model = BrandProfile
    can_delete = False


class InfluencerProfileInline(admin.StackedInline):
    model = InfluencerProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [BrandProfileInline, InfluencerProfileInline]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Brand)
admin.site.register(Influencer)
admin.site.register(Niche)
admin.site.register(AgeBracket)
admin.site.register(Platform)
admin.site.register(Language)
admin.site.register(Gender)
admin.site.register(InfluencerType)
admin.site.register(CompanySize)
admin.site.register(InfluencerPool)
admin.site.register(Campaign)
admin.site.register(Job)

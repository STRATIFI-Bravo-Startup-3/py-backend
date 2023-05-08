from django.contrib import admin
from .models import SocialMediaPlatform, SocialMediaHandle, CustomURL

@admin.register(SocialMediaPlatform)
class SocialMediaPlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_endpoint')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    fields = ('name', 'api_endpoint')


@admin.register(SocialMediaHandle)
class SocialMediaHandleAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'handle', 'followers')
    search_fields = ('user__username', 'handle')
    list_filter = ('platform__name',)
    ordering = ('user__username',)
    fields = ('user', 'platform', 'handle', 'followers', 'custom_followers', 'urls', 'custom_url', 'last_updated')
    
    
@admin.register(CustomURL)
class CustomURLAdmin(admin.ModelAdmin):
    list_display = ('url',)
    search_fields = ('url',)
    ordering = ('url',)


from django.contrib import admin


from .models import About, Vision, Mission, Goal, Service

'''class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "body",)
    prepopulated_fields = {"slug": ("title",)}'''

class AboutAdmin(admin.ModelAdmin):
    readonly_fields = ()

class VisionAdmin(admin.ModelAdmin):
    readonly_fields = ()

class MissionAdmin(admin.ModelAdmin):
    readonly_fields = ()

class GoalAdmin(admin.ModelAdmin):
    readonly_fields = ()

class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ()

#admin.site.register(Page, PageAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(Vision, VisionAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Service, ServiceAdmin)

from django.contrib import admin


from .models import Page 

class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "body",)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Page, PageAdmin)
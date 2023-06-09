from django.contrib import admin
from blog.models import BlogPost, Comment



class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "owner", "created_at"]
	list_display_links = ["created_at"]
	list_editable = ["title"]
	list_filter = ["created_at", "draft"]
	prepopulated_fields = {"slug": ("title",)}
	search_fields = ["title", "content"]
	class Meta:
		model = BlogPost


admin.site.register(BlogPost, PostModelAdmin)
admin.site.register(Comment)
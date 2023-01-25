from django.contrib import admin
from blog.models import BlogPost,Comments



class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "owner", "created_at"]
	list_display_links = ["created_at"]
	list_editable = ["title"]
	list_filter = ["created_at", "draft"]

	search_fields = ["title", "content"]
	class Meta:
		model = BlogPost


admin.site.register(BlogPost, PostModelAdmin)
admin.site.register(Comments)

'''from django.contrib import admin
from blog.models import Post, Category, Comment

class PostAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)'''
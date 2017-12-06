from django.contrib import admin
from .models import Post 
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["id", "title", "timestamp", "updated", "draft", "publish"]
	search_fields = ["title", "content"]
	list_filter = ["timestamp"]
	list_display_links = ["title"]
	#list_editable
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)
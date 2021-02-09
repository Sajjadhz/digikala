from django.contrib import admin

# Register your models here.
from siteview.models import SlideShow


class SlideShowItemsAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'action_text', 'action_url')
    search_fields = ('title', 'subtitle')
    list_filter = ('title',)


admin.site.register(SlideShow, SlideShowItemsAdmin)
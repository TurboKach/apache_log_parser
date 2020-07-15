from django.contrib import admin
from .models import Log


class LogAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-'
    list_display = (
        'ip_address',
        'created_date',
        'published_date',
        'http_method',
        'uri',
        'url',
        'urn',
        'response_code',
        'content_length',
        'browser'
    )
    fieldsets = (
        (None, {
            'fields': (
                'ip_address',
                'created_date',
                'published_date',
                'http_method',
            )
        }),
        ('URL', {
            'fields': (
                'uri',
                'url',
                'urn',
            )
        }),
        (None, {
            'fields': (
                'response_code',
                'content_length',
                'browser'
            )
        })
    )
    list_filter = ('created_date', )


admin.site.register(Log, LogAdmin)

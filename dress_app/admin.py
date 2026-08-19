from django.contrib import admin
from .models import StandardPrice, StudentDressEntry

@admin.register(StandardPrice)
class StandardPriceAdmin(admin.ModelAdmin):
    list_display = ('standard', 'dress_price', 'extra_dress_price', 'dupatta_price', 'extra_dupatta_price', 'updated_at')
    list_editable = ('dress_price', 'extra_dress_price', 'dupatta_price', 'extra_dupatta_price')
    ordering = ('standard',)


@admin.register(StudentDressEntry)
class StudentDressEntryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'standard', 'medium', 'package_model',
        'has_dress', 'has_dupatta', 'has_extra_dress', 'has_extra_dupatta',
        'total_price', 'created_at'
    )
    list_filter = ('standard', 'medium', 'package_model', 'has_dress', 'has_dupatta', 'has_extra_dress', 'has_extra_dupatta')
    search_fields = ('name', 'notes')
    ordering = ('-created_at',)

from django.contrib import admin
from .models import Users, DocCategory, Documents, FileActivityLogs

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'role_status', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role_status', 'date_joined')
    readonly_fields = ('date_joined',)


@admin.register(DocCategory)
class DocCategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_id', 'cat_name', 'created_at', 'updated_at')
    search_fields = ('cat_name',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'title', 'user', 'category', 'status', 'expiration_date', 'uploaded_at')
    search_fields = ('title', 'description', 'document_number')
    list_filter = ('status', 'category', 'uploaded_at', 'expiration_date')
    readonly_fields = ('uploaded_at', 'updated_at')
    fieldsets = (
        ('Document Information', {
            'fields': ('user', 'category', 'title', 'description', 'document_number')
        }),
        ('Dates', {
            'fields': ('issue_date', 'expiration_date')
        }),
        ('File & Status', {
            'fields': ('file_path', 'status')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FileActivityLogs)
class FileActivityLogsAdmin(admin.ModelAdmin):
    list_display = ('log_id', 'user', 'name_file', 'timestamp')
    search_fields = ('name_file', 'description')
    list_filter = ('timestamp', 'user')
    readonly_fields = ('timestamp',)

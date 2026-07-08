from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
import os

class Users(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('user', 'User'),
        ('viewer', 'Viewer'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role_status = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class DocCategory(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Document Categories"

    def __str__(self):
        return self.cat_name


class Documents(models.Model):
    STATUS_CHOICES = [
        ('valid', 'Valid'),
        ('expiring_soon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('archived', 'Archived'),
    ]
    
    EXPIRATION_STATUS_DISPLAY = {
        'valid': '✅ Valid',
        'expiring_soon': '⚠️ Expiring Soon',
        'expired': '❌ Expired',
        'archived': '📦 Archived',
    }
    
    document_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    category = models.ForeignKey(DocCategory, on_delete=models.CASCADE, db_column='category_id')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    document_number = models.CharField(max_length=100, blank=True, null=True, help_text="Optional: ID number, passport number, etc.")
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    issue_date = models.DateField(null=True, blank=True, help_text="When was this document issued?")
    expiration_date = models.DateField(null=True, blank=True, help_text="When does this document expire?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='valid')

    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['expiration_date']),
        ]

    def __str__(self):
        return self.title
    
    def get_expiration_status(self):
        """Calculate document expiration status based on dates"""
        if self.status == 'archived':
            return 'archived'
        
        if not self.expiration_date:
            return 'valid'
        
        today = timezone.now().date()
        days_until_expiration = (self.expiration_date - today).days
        
        if days_until_expiration < 0:
            return 'expired'
        elif days_until_expiration <= 30:  # Warning threshold: 30 days
            return 'expiring_soon'
        else:
            return 'valid'
    
    def update_status(self):
        """Update status based on expiration date"""
        new_status = self.get_expiration_status()
        if self.status != new_status and self.status != 'archived':
            self.status = new_status
            self.save()
    
    def is_expired(self):
        """Check if document has expired"""
        if not self.expiration_date:
            return False
        return self.expiration_date < timezone.now().date()
    
    def is_expiring_soon(self):
        """Check if document will expire within 30 days"""
        if not self.expiration_date:
            return False
        today = timezone.now().date()
        days_until = (self.expiration_date - today).days
        return 0 <= days_until <= 30
    
    def days_until_expiration(self):
        """Get number of days until expiration"""
        if not self.expiration_date:
            return None
        return (self.expiration_date - timezone.now().date()).days
    
    def get_file_extension(self):
        """Get file extension"""
        return os.path.splitext(self.file_path)[1].lower()
    
    def is_previewable(self):
        """Check if file can be previewed"""
        ext = self.get_file_extension()
        previewable = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp']
        return ext in previewable


class FileActivityLogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    description = models.TextField()
    name_file = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    old_file = models.CharField(max_length=255, blank=True, null=True)
    new_file = models.CharField(max_length=255, blank=True, null=True)
    old_file_path = models.CharField(max_length=255, blank=True, null=True)
    new_file_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "File Activity Logs"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Log #{self.log_id} - User {self.user_id}"
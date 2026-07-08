from django import forms
from .models import Users, DocCategory, Documents, FileActivityLogs

class UserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label='Confirm Password')
    
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password', 'role_status']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
            'role_status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class DocCategoryForm(forms.ModelForm):
    class Meta:
        model = DocCategory
        fields = ['cat_name', 'description']
        widgets = {
            'cat_name': forms.TextInput(attrs={'placeholder': 'Category Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 4}),
        }


class DocumentForm(forms.ModelForm):
    # File upload field (not in model, for upload simulation)
    document_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png,.docx,.xlsx,.txt',
            'id': 'file-upload'
        }),
        help_text='Supported: PDF, JPG, PNG, DOCX, XLSX, TXT'
    )
    
    class Meta:
        model = Documents
        fields = ['user', 'category', 'title', 'description', 'document_number', 'file_path', 'issue_date', 'expiration_date', 'status']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g., My Passport', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Additional notes about this document...', 'class': 'form-control', 'rows': 3}),
            'document_number': forms.TextInput(attrs={'placeholder': 'Passport, ID, License number etc.', 'class': 'form-control'}),
            'file_path': forms.TextInput(attrs={'placeholder': 'File will be uploaded', 'class': 'form-control', 'readonly': 'readonly'}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_document_file(self):
        file = self.cleaned_data.get('document_file')
        if file:
            # Validate file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must not exceed 10MB")
            
            # Validate file extension
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.docx', '.xlsx', '.txt']
            import os
            file_ext = os.path.splitext(file.name)[1].lower()
            if file_ext not in allowed_extensions:
                raise forms.ValidationError(f"File type '{file_ext}' not supported. Allowed: {', '.join(allowed_extensions)}")
        
        return file


class FileActivityLogsForm(forms.ModelForm):
    class Meta:
        model = FileActivityLogs
        fields = ['user', 'description', 'name_file', 'old_file', 'new_file', 'old_file_path', 'new_file_path']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 3}),
            'name_file': forms.TextInput(attrs={'placeholder': 'File Name', 'class': 'form-control'}),
            'old_file': forms.TextInput(attrs={'placeholder': 'Old File Name', 'class': 'form-control'}),
            'new_file': forms.TextInput(attrs={'placeholder': 'New File Name', 'class': 'form-control'}),
            'old_file_path': forms.TextInput(attrs={'placeholder': 'Old File Path', 'class': 'form-control'}),
            'new_file_path': forms.TextInput(attrs={'placeholder': 'New File Path', 'class': 'form-control'}),
        }
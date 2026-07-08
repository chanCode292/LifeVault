from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Users, DocCategory, Documents, FileActivityLogs
from .forms import UserForm, DocCategoryForm, DocumentForm, FileActivityLogsForm

def login_view(request):
    if request.method == "POST":
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        try:
            user = Users.objects.get(email=email_input)
            if user.check_password(password_input):
                request.session['user_id'] = user.user_id
                request.session['user_email'] = user.email
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials.")
        except Users.DoesNotExist:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

def register_view(request):
    form = UserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully! Please sign in.")
        return redirect('login')
    return render(request, 'register.html', {'form': form})

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Get all documents
    all_documents = Documents.objects.all().select_related('user', 'category')
    
    # Update status for all documents
    for doc in all_documents:
        doc.update_status()
    
    # Get statistics
    expiring_soon = all_documents.filter(status='expiring_soon')
    expired = all_documents.filter(status='expired')
    valid = all_documents.filter(status='valid')
    recent_documents = all_documents.order_by('-uploaded_at')[:5]
    
    context = {
        'total_docs': all_documents.count(),
        'total_categories': DocCategory.objects.count(),
        'total_users': Users.objects.count(),
        'total_logs': FileActivityLogs.objects.count(),
        'expiring_soon_count': expiring_soon.count(),
        'expired_count': expired.count(),
        'valid_count': valid.count(),
        'expiring_soon_docs': expiring_soon[:5],
        'expired_docs': expired[:5],
        'recent_documents': recent_documents,
    }
    
    return render(request, 'dashboard.html', context)

def search_documents(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    results = None
    search_query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'title')
    
    if search_query:
        if search_type == 'title':
            results = Documents.objects.filter(title__icontains=search_query)
        elif search_type == 'category':
            results = Documents.objects.filter(category__cat_name__icontains=search_query)
        elif search_type == 'document_number':
            results = Documents.objects.filter(document_number__icontains=search_query)
        else:
            results = Documents.objects.filter(
                title__icontains=search_query
            ) | Documents.objects.filter(
                document_number__icontains=search_query
            )
        
        # Update status for all results
        for doc in results:
            doc.update_status()
        
        results = results.select_related('user', 'category').order_by('-uploaded_at')
    
    return render(request, 'search_results.html', {
        'results': results,
        'search_query': search_query,
        'search_type': search_type,
    })

def logout_view(request):
    request.session.flush()
    return redirect('login')

def upload_document(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    form = DocumentForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        document = form.save(commit=False)
        
        # Handle file upload
        if 'document_file' in request.FILES:
            uploaded_file = request.FILES['document_file']
            # Store file info in file_path (can be enhanced later for actual file storage)
            document.file_path = f"uploads/{uploaded_file.name}"
        
        # Auto-update status based on dates
        document.update_status()
        document.save()
        
        # Log activity
        FileActivityLogs.objects.create(
            user_id=document.user.user_id,
            description=f"Uploaded document: {document.title}",
            name_file=document.file_path,
            old_file="",
            new_file=document.file_path
        )
        
        messages.success(request, f"Document '{document.title}' uploaded successfully!")
        return redirect('manage_documents')
    
    return render(request, 'upload_document.html', {'form': form})

def document_detail(request, doc_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    document = get_object_or_404(Documents, document_id=doc_id)
    document.update_status()  # Update status before displaying
    
    return render(request, 'document_detail.html', {'document': document})

def how_it_works(request):
    """Display the workflow and features page"""
    return render(request, 'how_it_works.html')

# ===== DOCUMENT CATEGORY VIEWS =====
def manage_categories(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    categories = DocCategory.objects.all()
    form = DocCategoryForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Category created successfully!")
        return redirect('manage_categories')
    
    return render(request, 'categories.html', {'categories': categories, 'form': form})

def edit_category(request, cat_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    category = get_object_or_404(DocCategory, cat_id=cat_id)
    form = DocCategoryForm(request.POST or None, instance=category)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully!")
        return redirect('manage_categories')
    
    return render(request, 'edit_category.html', {'form': form, 'category': category})

def delete_category(request, cat_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    category = get_object_or_404(DocCategory, cat_id=cat_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('manage_categories')
    
    return render(request, 'confirm_delete.html', {'item': category, 'item_type': 'Category'})

# ===== DOCUMENT VIEWS =====
def manage_documents(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    documents = Documents.objects.all().select_related('user', 'category')
    form = DocumentForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Document created successfully!")
        return redirect('manage_documents')
    
    return render(request, 'documents.html', {'documents': documents, 'form': form})

def edit_document(request, doc_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    document = get_object_or_404(Documents, document_id=doc_id)
    form = DocumentForm(request.POST or None, instance=document)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Document updated successfully!")
        return redirect('manage_documents')
    
    return render(request, 'edit_document.html', {'form': form, 'document': document})

def delete_document(request, doc_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    document = get_object_or_404(Documents, document_id=doc_id)
    if request.method == 'POST':
        document.delete()
        messages.success(request, "Document deleted successfully!")
        return redirect('manage_documents')
    
    return render(request, 'confirm_delete.html', {'item': document, 'item_type': 'Document'})

# ===== FILE ACTIVITY LOGS VIEWS =====
def manage_logs(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    logs = FileActivityLogs.objects.all().select_related('user').order_by('-timestamp')
    form = FileActivityLogsForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Log entry created successfully!")
        return redirect('manage_logs')
    
    return render(request, 'logs.html', {'logs': logs, 'form': form})

def view_log(request, log_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    log = get_object_or_404(FileActivityLogs, log_id=log_id)
    return render(request, 'view_log.html', {'log': log})

def delete_log(request, log_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    log = get_object_or_404(FileActivityLogs, log_id=log_id)
    if request.method == 'POST':
        log.delete()
        messages.success(request, "Log entry deleted successfully!")
        return redirect('manage_logs')
    
    return render(request, 'confirm_delete.html', {'item': log, 'item_type': 'Log Entry'})

# ===== USER MANAGEMENT VIEWS =====
def manage_users(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    users = Users.objects.all()
    form = UserForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "User created successfully!")
        return redirect('manage_users')
    
    return render(request, 'users.html', {'users': users, 'form': form})

def edit_user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user = get_object_or_404(Users, user_id=user_id)
    form = UserForm(request.POST or None, instance=user)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "User updated successfully!")
        return redirect('manage_users')
    
    return render(request, 'edit_user.html', {'form': form, 'user': user})

def delete_user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user = get_object_or_404(Users, user_id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('manage_users')
    
    return render(request, 'confirm_delete.html', {'item': user, 'item_type': 'User'})
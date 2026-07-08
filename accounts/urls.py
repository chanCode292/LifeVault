from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("search/", views.search_documents, name="search"),
    path("how-it-works/", views.how_it_works, name="how_it_works"),
    
    # Document Upload & Detail
    path("documents/upload/", views.upload_document, name="upload_document"),
    path("documents/<int:doc_id>/", views.document_detail, name="document_detail"),
    
    # Categories
    path("dashboard/categories/", views.manage_categories, name="manage_categories"),
    path("dashboard/categories/edit/<int:cat_id>/", views.edit_category, name="edit_category"),
    path("dashboard/categories/delete/<int:cat_id>/", views.delete_category, name="delete_category"),
    
    # Documents
    path("dashboard/documents/", views.manage_documents, name="manage_documents"),
    path("dashboard/documents/edit/<int:doc_id>/", views.edit_document, name="edit_document"),
    path("dashboard/documents/delete/<int:doc_id>/", views.delete_document, name="delete_document"),
    
    # Logs
    path("dashboard/logs/", views.manage_logs, name="manage_logs"),
    path("dashboard/logs/view/<int:log_id>/", views.view_log, name="view_log"),
    path("dashboard/logs/delete/<int:log_id>/", views.delete_log, name="delete_log"),
    
    # Users
    path("dashboard/users/", views.manage_users, name="manage_users"),
    path("dashboard/users/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("dashboard/users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
]
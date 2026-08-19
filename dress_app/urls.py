from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_view, name='entry'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('viewer/', views.viewer_view, name='viewer'),
    path('entry/edit/<int:pk>/', views.edit_entry_view, name='edit_entry'),
    path('entry/delete/<int:pk>/', views.delete_entry_view, name='delete_entry'),
    path('export/pdf/', views.export_pdf_view, name='export_pdf'),
    path('export/excel/', views.export_excel_view, name='export_excel'),
    path('api/standard-price/<int:std>/', views.get_standard_price_api, name='api_standard_price'),
]

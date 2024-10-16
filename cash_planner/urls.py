from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'), 
    path('index/', views.index, name='index_home'),
    path('add/', views.add_expense, name='add_expense'),
    path('list/', views.expense_list, name='expense_list'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('income/add/', views.add_income, name="add_income"),
    path('income/list/', views.income_list, name="income_list"),
    path('income/edit/<int:pk>/', views.edit_income, name="edit_income"),
    path('income/delete/<int:pk>/', views.delete_income, name="delete_income"),
    path('patience/add/', views.add_patience, name='add_patience'),
    path('patience/list/', views.patience_list, name='patience_list'),
    path('patience/edit/<int:pk>/', views.edit_patience, name="edit_patience"),
    path('patience/delete/<int:pk>/', views.delete_patience, name="delete_patience"),
    path('budget/graph/<int:year>/<int:month>/', views.expense_graph, name='expense_graph'),
    path('add_main_category/', views.add_main_category, name='add_main_category'),
    path('main_category_list/', views.main_category_list, name='main_category_list'),
    path('edit_main_category/<int:pk>/', views.edit_main_category, name="edit_main_category"),
    path('delete_main_category/<int:pk>/', views.delete_main_category, name="delete_main_category"),
    path('add_sub_category/', views.add_sub_category, name='add_sub_category'),
    path('sub_category_list/', views.sub_category_list, name='sub_category_list'),
    path('edit_sub_category/<int:pk>/', views.edit_sub_category, name="edit_sub_category"),
    path('delete_sub_category/<int:pk>/', views.delete_sub_category, name="delete_sub_category"),
    path('add_source/', views.add_source, name='add_source'),
    path('source_list/', views.source_list, name='source_list'),
    path('edit_source/<int:pk>/', views.edit_source, name="edit_source"),
    path('delete_source/<int:pk>/', views.delete_source, name="delete_source"),
    path('export_expense_csv/', views.export_expense_csv, name='export_expense_csv'),  # 支出CSVエクスポート
    path('export_income_csv/', views.export_income_csv, name='export_income_csv'),  # 収入CSVエクスポート
    path('export_smart_save_csv/', views.export_smart_save_csv, name='export_smart_save_csv'),  # スマートセーブCSVエクスポート
    path('user_info/', views.user_info, name='user_info'),
    path('submit_user_info/', views.submit_user_info, name='submit_user_info'),
    path('user_storage/', views.user_storage, name='user_storage'),
]

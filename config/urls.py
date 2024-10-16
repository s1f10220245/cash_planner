from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cash_planner.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Django の認証ビューを使用
]

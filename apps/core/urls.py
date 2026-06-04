from django.urls import path

from .views import DashboardView, home, superadmin_backup, superadmin_dashboard, superadmin_restore

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("superadmin/", superadmin_dashboard, name="superadmin_dashboard"),
    path("superadmin/backup/", superadmin_backup, name="superadmin_backup"),
    path("superadmin/restore/", superadmin_restore, name="superadmin_restore"),
]

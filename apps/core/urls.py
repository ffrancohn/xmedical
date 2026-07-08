from django.urls import path

from .views import (
    AuditoriaListView,
    DashboardView,
    home,
    superadmin_backup,
    superadmin_dashboard,
    superadmin_export_tenant,
    superadmin_import_tenant,
    superadmin_restore,
)

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("auditoria/", AuditoriaListView.as_view(), name="auditoria_lista"),
    path("superadmin/", superadmin_dashboard, name="superadmin_dashboard"),
    path("superadmin/backup/", superadmin_backup, name="superadmin_backup"),
    path("superadmin/restore/", superadmin_restore, name="superadmin_restore"),
    path("superadmin/tenant/<int:institucion_id>/exportar/", superadmin_export_tenant, name="superadmin_export_tenant"),
    path("superadmin/tenant/importar/", superadmin_import_tenant, name="superadmin_import_tenant"),
]

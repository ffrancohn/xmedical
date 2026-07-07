from django.db import migrations

RLS_TABLES = [
    "ia_predictiva_prediccionausentismo",
    "ia_predictiva_demandacita",
    "ia_predictiva_alertariesgocronico",
]

POLICY_SQL = """
CREATE POLICY tenant_isolation ON {table}
    FOR ALL
    USING (
        institucion_id = get_current_institucion_id()
        OR get_current_institucion_id() IS NULL
    )
    WITH CHECK (
        institucion_id = get_current_institucion_id()
        OR get_current_institucion_id() IS NULL
    );
"""


def enable_rls(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        for table in RLS_TABLES:
            cursor.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
            cursor.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
            cursor.execute(f"DROP POLICY IF EXISTS tenant_isolation ON {table}")
            cursor.execute(POLICY_SQL.format(table=table))


def disable_rls(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        for table in RLS_TABLES:
            cursor.execute(f"DROP POLICY IF EXISTS tenant_isolation ON {table}")
            cursor.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_pacientes_ocr_rls"),
        ("ia_predictiva", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(enable_rls, disable_rls),
    ]

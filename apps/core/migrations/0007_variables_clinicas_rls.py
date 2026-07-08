from django.db import migrations

RLS_TABLES = [
    "variables_clinicas_variableclinica",
    "variables_clinicas_valorvariableclinica",
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
        ("core", "0006_qr_rls"),
        ("variables_clinicas", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(enable_rls, disable_rls),
    ]

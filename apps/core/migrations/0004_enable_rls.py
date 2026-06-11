from django.db import migrations

RLS_TABLES = [
    "core_especialidad",
    "core_profesional",
    "core_horario",
    "core_logauditoria",
    "pacientes_paciente",
    "citas_cita",
    "preclinica_preclinica",
    "consulta_consulta",
    "consulta_diagnostico",
]

FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION get_current_institucion_id()
RETURNS INTEGER AS $$
DECLARE
    val TEXT;
BEGIN
    val := current_setting('app.current_institucion_id', true);
    IF val IS NULL OR val = '' THEN
        RETURN NULL;
    END IF;
    RETURN val::INTEGER;
EXCEPTION
    WHEN OTHERS THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;
"""

REVERSE_FUNCTION_SQL = "DROP FUNCTION IF EXISTS get_current_institucion_id();"


def enable_rls(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(FUNCTION_SQL)
        for table in RLS_TABLES:
            cursor.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
            cursor.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
            cursor.execute(f"DROP POLICY IF EXISTS tenant_isolation ON {table}")
            cursor.execute(
                f"""
                CREATE POLICY tenant_isolation ON {table}
                    FOR ALL
                    USING (
                        institucion_id = get_current_institucion_id()
                        OR get_current_institucion_id() IS NULL
                    )
                    WITH CHECK (
                        institucion_id = get_current_institucion_id()
                        OR get_current_institucion_id() IS NULL
                    )
                """
            )


def disable_rls(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    with schema_editor.connection.cursor() as cursor:
        for table in RLS_TABLES:
            cursor.execute(f"DROP POLICY IF EXISTS tenant_isolation ON {table}")
            cursor.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
        cursor.execute(REVERSE_FUNCTION_SQL)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_fase1_cierre"),
        ("citas", "0002_fase1_cierre"),
        ("pacientes", "0002_contacto_extendido"),
        ("preclinica", "0001_initial"),
        ("consulta", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(enable_rls, disable_rls),
    ]

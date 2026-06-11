from django.db import connection


def set_institucion_rls(institucion_id):
    with connection.cursor() as cursor:
        if institucion_id is None:
            cursor.execute("RESET app.current_institucion_id")
        else:
            cursor.execute(
                "SELECT set_config('app.current_institucion_id', %s, false)",
                [str(institucion_id)],
            )

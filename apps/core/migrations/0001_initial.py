from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Institucion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=200)),
                ("subdominio", models.CharField(max_length=100, unique=True)),
                ("tipo", models.CharField(choices=[("privada", "Privada"), ("publica", "Publica")], max_length=50)),
                ("configuracion", models.JSONField(blank=True, default=dict)),
                ("activo", models.BooleanField(default=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
            ],
            options={"verbose_name_plural": "instituciones"},
        ),
        migrations.CreateModel(
            name="Especialidad",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100)),
                ("codigo", models.CharField(blank=True, max_length=20)),
                ("nivel", models.CharField(choices=[("primero", "Primer Nivel"), ("segundo", "Segundo Nivel")], max_length=20)),
                ("duracion_consulta_minutos", models.IntegerField(default=20)),
                ("activo", models.BooleanField(default=True)),
                ("institucion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.institucion")),
            ],
            options={"unique_together": {("institucion", "nombre")}},
        ),
        migrations.CreateModel(
            name="Profesional",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100)),
                ("tipo", models.CharField(choices=[("admin", "Admin"), ("medico", "Medico"), ("enfermera", "Enfermera"), ("recepcionista", "Recepcionista")], max_length=20)),
                ("registro_medico", models.CharField(blank=True, max_length=50)),
                ("activo", models.BooleanField(default=True)),
                ("especialidad", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="core.especialidad")),
                ("institucion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.institucion")),
                ("usuario", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Horario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("dia_semana", models.IntegerField(choices=[(0, "Lunes"), (1, "Martes"), (2, "Miercoles"), (3, "Jueves"), (4, "Viernes"), (5, "Sabado"), (6, "Domingo")])),
                ("hora_inicio", models.TimeField()),
                ("hora_fin", models.TimeField()),
                ("activo", models.BooleanField(default=True)),
                ("institucion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.institucion")),
                ("profesional", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.profesional")),
            ],
            options={"unique_together": {("profesional", "dia_semana", "hora_inicio", "hora_fin")}},
        ),
    ]

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("citas", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Consulta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("motivo_consulta", models.TextField(blank=True)),
                ("anamnesis", models.TextField(blank=True)),
                ("examen_fisico", models.TextField(blank=True)),
                ("plan_terapeutico", models.TextField(blank=True)),
                ("conducta", models.CharField(choices=[("alta", "Alta medica"), ("cita_subsiguiente", "Cita subsiguiente"), ("referencia", "Referencia")], default="alta", max_length=50)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("cita", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="citas.cita")),
                ("institucion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.institucion")),
            ],
        ),
        migrations.CreateModel(
            name="Diagnostico",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo_cie10", models.CharField(max_length=10)),
                ("nombre", models.CharField(max_length=200)),
                ("es_principal", models.BooleanField(default=False)),
                ("orden", models.IntegerField(default=1)),
                ("consulta", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="diagnosticos", to="consulta.consulta")),
                ("institucion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.institucion")),
            ],
            options={"ordering": ["orden", "id"]},
        ),
    ]

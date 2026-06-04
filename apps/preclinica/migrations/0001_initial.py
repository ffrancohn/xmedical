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
            name="Preclinica",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("presion_arterial_sis", models.IntegerField(blank=True, null=True)),
                ("presion_arterial_dia", models.IntegerField(blank=True, null=True)),
                ("frecuencia_cardiaca", models.IntegerField(blank=True, null=True)),
                ("temperatura", models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ("saturacion_o2", models.IntegerField(blank=True, null=True)),
                ("peso", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("talla", models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ("imc", models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ("motivo_consulta", models.TextField(blank=True)),
                ("triaje", models.CharField(blank=True, choices=[("baja", "Baja"), ("media", "Media"), ("alta", "Alta")], max_length=20, null=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("cita", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="citas.cita")),
                ("institucion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.institucion")),
            ],
        ),
    ]

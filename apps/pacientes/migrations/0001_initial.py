from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Paciente",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("documento", models.CharField(max_length=20)),
                ("nombre", models.CharField(max_length=100)),
                ("apellido", models.CharField(max_length=100)),
                ("fecha_nacimiento", models.DateField(blank=True, null=True)),
                ("sexo", models.CharField(blank=True, choices=[("M", "Masculino"), ("F", "Femenino"), ("OTRO", "Otro")], max_length=10)),
                ("telefono", models.CharField(blank=True, max_length=20)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("activo", models.BooleanField(default=True)),
                ("institucion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.institucion")),
            ],
            options={"ordering": ["apellido", "nombre"], "unique_together": {("institucion", "documento")}},
        ),
    ]

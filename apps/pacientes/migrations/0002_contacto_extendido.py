from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pacientes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="paciente",
            name="telefono_fijo",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="paciente",
            name="direccion",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="paciente",
            name="ciudad",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="paciente",
            name="departamento",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="paciente",
            name="contacto_emergencia_nombre",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="paciente",
            name="contacto_emergencia_telefono",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="paciente",
            name="observaciones",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="paciente",
            name="telefono",
            field=models.CharField(blank=True, max_length=20, verbose_name="telefono movil"),
        ),
    ]

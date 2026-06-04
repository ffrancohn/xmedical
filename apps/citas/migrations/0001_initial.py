from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
        ("pacientes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cita",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateField()),
                ("hora", models.TimeField()),
                ("estado", models.CharField(choices=[("pendiente", "Pendiente"), ("confirmada", "Confirmada"), ("cancelada", "Cancelada"), ("atendida", "Atendida")], default="pendiente", max_length=20)),
                ("tipo_agendamiento", models.CharField(choices=[("especifico", "Especifico"), ("flexible", "Flexible")], default="especifico", max_length=20)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("institucion", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.institucion")),
                ("paciente", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="pacientes.paciente")),
                ("profesional", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.profesional")),
            ],
            options={"ordering": ["fecha", "hora"], "unique_together": {("profesional", "fecha", "hora")}},
        ),
    ]

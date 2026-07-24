from django.db import migrations, models


def migrar_vital_a_garden(apps, schema_editor):
    UserPreference = apps.get_model("auth_app", "UserPreference")
    UserPreference.objects.filter(theme="vital").update(theme="garden")


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0002_tema_vital_default"),
    ]

    operations = [
        migrations.RunPython(migrar_vital_a_garden, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="userpreference",
            name="theme",
            field=models.CharField(
                choices=[
                    ("garden", "Garden"),
                    ("emerald", "Esmeralda"),
                    ("aqua", "Aqua"),
                    ("corporate", "Corporativo"),
                    ("light", "Claro"),
                    ("dark", "Oscuro"),
                    ("cupcake", "Suave"),
                    ("bumblebee", "Amarillo"),
                    ("winter", "Invierno"),
                    ("night", "Noche"),
                    ("forest", "Bosque"),
                    ("lofi", "Minimalista"),
                ],
                default="garden",
                max_length=30,
            ),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0003_remove_tema_vital"),
    ]

    operations = [
        migrations.AddField(
            model_name="userpreference",
            name="interface_mode",
            field=models.CharField(
                choices=[
                    ("classic", "Clásica (sidebar DaisyUI)"),
                    ("atlas", "Atlas (isométrica, estilo prototipo)"),
                ],
                default="classic",
                max_length=20,
            ),
        ),
    ]

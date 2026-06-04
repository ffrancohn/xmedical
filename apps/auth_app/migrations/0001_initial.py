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
            name="UserPreference",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("theme", models.CharField(choices=[("garden", "Garden"), ("light", "Claro"), ("dark", "Oscuro"), ("corporate", "Corporativo"), ("emerald", "Esmeralda"), ("cupcake", "Suave"), ("bumblebee", "Amarillo"), ("winter", "Invierno"), ("night", "Noche"), ("forest", "Bosque"), ("aqua", "Aqua"), ("lofi", "Minimalista")], default="garden", max_length=30)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="preference", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

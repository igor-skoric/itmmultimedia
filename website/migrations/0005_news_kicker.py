from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_video_project_fields"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="newsarticle",
            options={
                "ordering": ["-published_at", "-id"],
                "verbose_name": "aktuelnost",
                "verbose_name_plural": "aktuelnosti",
            },
        ),
        migrations.AddField(
            model_name="newsarticle",
            name="kicker",
            field=models.CharField(
                blank=True,
                choices=[
                    ("gallery", "Galerija"),
                    ("video", "Video"),
                    ("interview", "Intervju"),
                    ("field", "Teren"),
                    ("in_progress", "U radu"),
                ],
                max_length=20,
            ),
        ),
    ]

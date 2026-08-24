from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="partner",
            name="logo_url",
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="partner",
            name="image_url",
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="partner",
            name="description_sr",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="partner",
            name="description_en",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="partner",
            name="description_fr",
            field=models.TextField(blank=True),
        ),
    ]

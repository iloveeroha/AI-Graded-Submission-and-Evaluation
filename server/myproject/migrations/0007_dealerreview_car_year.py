from django.db import migrations, models


def populate_demo_car_year(apps, schema_editor):
    DealerReview = apps.get_model("myproject", "DealerReview")
    database = schema_editor.connection.alias
    DealerReview.objects.using(database).filter(
        reviewer_name="Jordan Lee",
        comment="Helpful staff and a smooth buying experience.",
        car_make="Toyota",
        car_model="Camry",
        car_year__isnull=True,
    ).update(car_year=2025)


class Migration(migrations.Migration):
    dependencies = [
        ("myproject", "0006_seed_course_demo_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="dealerreview",
            name="car_year",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.RunPython(
            populate_demo_car_year,
            migrations.RunPython.noop,
        ),
    ]

from datetime import date

from django.db import migrations


def seed_course_demo_data(apps, schema_editor):
    Dealer = apps.get_model("myproject", "Dealer")
    DealerReview = apps.get_model("myproject", "DealerReview")
    CarMake = apps.get_model("myproject", "CarMake")
    CarModel = apps.get_model("myproject", "CarModel")
    database = schema_editor.connection.alias

    dealer, _created = Dealer.objects.using(database).get_or_create(
        name="Example Coursera Auto Center",
        defaults={
            "city": "Wichita",
            "state": "KS",
            "address": "100 Learning Way",
            "zip": "67202",
            "latitude": 37.6872,
            "longitude": -97.3301,
            "short_name": "Example Auto",
            "full_name": "Example Coursera Auto Center of Wichita",
        },
    )
    DealerReview.objects.using(database).get_or_create(
        dealer_id=dealer.pk,
        reviewer_name="Jordan Lee",
        comment="Helpful staff and a smooth buying experience.",
        defaults={
            "rating": 5,
            "purchase": True,
            "purchase_date": date(2025, 1, 15),
            "car_make": "Toyota",
            "car_model": "Camry",
            "sentiment": "positive",
        },
    )

    models_by_make = {
        "Honda": ["Accord", "Civic", "CR-V"],
        "Nissan": ["Altima", "LEAF", "Rogue"],
        "Subaru": ["Crosstrek", "Forester", "Impreza"],
        "Toyota": ["Camry", "Corolla", "Prius"],
        "Volkswagen": ["Golf", "Jetta", "Tiguan"],
    }
    for make_name, model_names in models_by_make.items():
        make, _created = CarMake.objects.using(database).get_or_create(
            name=make_name
        )
        for model_name in model_names:
            CarModel.objects.using(database).get_or_create(
                make_id=make.pk,
                name=model_name,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("myproject", "0005_dealer_full_name_dealer_latitude_dealer_longitude_and_more"),
    ]

    operations = [
        migrations.RunPython(
            seed_course_demo_data,
            migrations.RunPython.noop,
        ),
    ]

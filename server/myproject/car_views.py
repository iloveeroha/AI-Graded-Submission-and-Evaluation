from django.http import JsonResponse
from django.views.decorators.http import require_GET

from myproject.models import CarMake


def serialize_cars():
    makes = CarMake.objects.prefetch_related("models")
    make_list = []
    model_list = []
    for make in makes:
        make_list.append({"id": make.id, "name": make.name})
        for model in make.models.all():
            model_list.append(
                {
                    "id": model.id,
                    "name": model.name,
                    "make": make.name,
                    "make_id": make.id,
                }
            )
    return make_list, model_list


@require_GET
def all_car_makes(request):
    makes = CarMake.objects.prefetch_related("models")
    return JsonResponse(
        {
            "count": makes.count(),
            "makes": [
                {
                    "id": make.id,
                    "name": make.name,
                    "models": [
                        {"id": model.id, "name": model.name}
                        for model in make.models.all()
                    ],
                }
                for make in makes
            ],
        }
    )


@require_GET
def cars_for_course(request):
    makes, models = serialize_cars()
    return JsonResponse({"CarMakes": makes, "CarModels": models})

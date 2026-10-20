from django.http import JsonResponse
from django.views.decorators.http import require_GET

from myproject.models import CarMake


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

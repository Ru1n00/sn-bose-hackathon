from .models import Category  # Import your Category model

def categories_processor(request):
    return {"categories": Category.objects.all()}

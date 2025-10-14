from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import PlantPage

# Render the list of plants 
def plant_list(request):
    """List all plants"""
    plants = PlantPage.objects.all()

    return render(request, 'plant_list.html', {'plants': plants})

# Render the detail view of a specific plant by ID or slug
def plant_detail(request, identifier):
    """Detail view for a specific plant by ID or slug"""
    # Try to get by ID first (if identifier is numeric)
    if identifier.isdigit():
        plant = get_object_or_404(PlantPage, id=int(identifier))
    else:
        # Otherwise treat as slug
        plant = get_object_or_404(PlantPage, slug=identifier)
    
    return render(request, 'plant_detail.html', {'plant': plant})

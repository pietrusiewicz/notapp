from django.shortcuts import get_object_or_404, render
#from django.template import loader

from .models import Category

def index(r):
    latest_categories_list = Category.objects.order_by('-last_usage')[:5]
    context = {
        'latest_categories_list': latest_categories_list,
    }
    return render(r, 'items/index.html', context)

def items(r, category_id):
    item = get_object_or_404(Category, pk=category_id)
    response = f"You're looking at items in category {category_id}"
    return render(r, 'items/items.html', {'item':item})


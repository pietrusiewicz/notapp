from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Category, Item

def index(r):
    latest_categories_list = Category.objects.order_by('-last_usage')[:5]
    context = {
        'latest_categories_list': latest_categories_list,
    }
    return render(r, 'items/index.html', context)

def items(r, category_id):
    cat = get_object_or_404(Category, pk=category_id)
    return render(r, 'items/items.html', {'category':cat})

def results(r, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(r, 'items/results.html', {'category': category})

def order(r, category_id):
    category = get_object_or_404(Category, pk=category_id)
    try:
        print(r.POST)
        selected_items = r.POST['item']
    except (KeyError, Item):
        return render(r, 'items/items.html', {
            'category': category,
            'error_message': "You picked nothing",
        })
    else:
        for item in category.item_set.all():
            if str(item.pk) in selected_items:
                item.price += 0.01
                item.save()
        return HttpResponseRedirect(reverse('items:results', args=(category_id,)))

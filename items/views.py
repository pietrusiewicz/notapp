from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView

from .models import Category, Item

class index(TemplateView):
    template_name = 'items/index.html'
    #context_object_name = 'latest_categories_list'

    def get_context_data(self):
        return {'latest_categories_list': Category.objects.all()}

class items(TemplateView):
    template_name = 'items/items.html'

    def get_context_data(self, **kwargs):
        cid = self.kwargs['category_id']
        cat = get_object_or_404(Category, pk=cid)
        return {'category': cat}

def results(r, category_id):
    template_name = 'items/results.html'

    def get_context_data(self, **kwargs):
        cid = self.kwargs['category_id']
        cat = get_object_or_404(Category, pk=cid)
        return {'category': cat}
    

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

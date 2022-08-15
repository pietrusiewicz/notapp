from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Category, Item, Order
from .forms import LoginForm, ChangePasswordForm, CreateUserForm, AddItemForm

#user = ''

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

class results(TemplateView):
    template_name = 'items/results.html'

    def get_context_data(self, **kwargs):
        cid = self.kwargs['category_id']
        cat = get_object_or_404(Category, pk=cid)
        return {'category': cat}

def add_to_cart(r):
    categoryid, item = r.POST['categoryid'], r.POST['item']
    if "cart" in r.session:
        r.session["cart"].append((categoryid, item))
    else:
        r.session["cart"] = [(categoryid, item)]

def profile(r):
    if 'usname' in r.session.keys():
    #except (KeyError):
        user = User.objects.get(username=r.session['usname'])
        orders = Order.objects.filter(pk=user.id)
        items = Item.objects.filter(owner=user)
        if not len(orders):
            orders = ""
        if not len(items):
            items = ""

        context = {
                'usname': user.username, 
                'orders': orders,
                'items': items
        }
        return render(r, 'items/profile.html', context)
    else:
        return HttpResponseRedirect('/sklapp/login/')

def add_item(r):
    if r.session['usname']:
        user = User.objects.get(username=r.session['usname'])
        if 'itemname' in r.POST and 'categoryid' in r.POST and 'price' in r.POST:
            category, itemname, price = r.POST['categoryid'], r.POST['itemname'], r.POST['price']
            c = Category.objects.get(id=category)
            c.item_set.create(owner=user, item_name=itemname,price=price)
            c.save()
            return HttpResponseRedirect('/sklapp/profile/')
        else:
            form = AddItemForm()
            context={'forms':form, 'categories':Category.objects.all()}
            return render(r, 'items/add_item.html', context)
    else:
        return HttpResponseRedirect('/sklapp/login/')

def login(r):
    form = LoginForm()
    context = {"forms":form}
    if 'usname' in r.POST and 'passwd' in r.POST:
    #if len(list(r.POST)) == 2:
        usname, passwd = r.POST['usname'],r.POST['passwd']
        user = authenticate(username=usname, password=passwd)
        # correct password
        if user:
            r.session['usname'] = str(user)
            return HttpResponseRedirect('/sklapp/profile/')
        # wrong password
        else:
            #return render(r, 'items/login.html', {"error_message": "Wrong Password"})
            #context = {"error_message": "Wrong password"}
            context["error_message"] = "Wrong password"
    else:
        context["error_message"] = "Fill empty brackets"
    return render(r, 'items/login.html', context)

def register(r):
    form = CreateUserForm()
    context= {"forms": form}
    # create an user
    fields = ['usname','email','passwd1','passwd2']
    condition=[s in r.POST for s in fields]
    if min(condition):
        username, email, passwd1, passwd2 = [r.POST[s] for s in fields]
        if username in User.objects.all():
            context["error_message"] = "User exists"
        elif passwd1 == passwd2:
            user = User.objects.create_user(username, email, password)
            user.save()
            return HttpResponseRedirect('/sklapp/login/')
        else:
            context["error_message"] = "passwords aren't the same"
    return render(r, 'items/register.html', context)

def change_password(r):
    usname = r.session['usname']
    form = ChangePasswordForm()
    context = {"forms": form}
    if 'passwd1' in r.POST and 'passwd2' in r.POST:
    #if len(r.POST.keys()) == 2:
    #if len(r.POST) == 2:
        if r.POST['passwd1'] == r.POST['passwd2']:
            passwd = r.POST["passwd1"]
            user = User(username=usname)
            user.set_password(passwd)
            return HttpResponseRedirect('/sklapp/profile/')
        else:
            #return render(r, 'items/change_password.html', {"error_message": "passwords are not the same"})
            context["error_message"]= "passwords are not the same"
    else:
        context["error_message"]= "Fill missing fields"
    return render(r, 'items/change_password.html', context)

def logout(r):
    r.session['usname']=''
    return HttpResponseRedirect('/sklapp/login/')

def order(r, category_id):
    category = get_object_or_404(Category, pk=category_id)
    try:
        selected_items = r.POST['item']
    except (KeyError, Item):
        return render(r, 'items/items.html', {
            'usname': r.session['usname'],
            'category': category,
            'error_message': "You picked nothing",
        })
    else:
        for item in category.item_set.all():
            if str(item.pk) in selected_items:
                item.price += 0.01
                item.save()
        return HttpResponseRedirect(reverse('items:results', args=(category_id,)))

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, base
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

from .models import Category, Item, Order, Cart
from .forms import LoginForm, ChangePasswordForm, CreateUserForm, AddItemForm

#user = ''

def get_cart_context(username):
    user = User.objects.get(username=username)
    orders = Order.objects.filter(user=user)
    items = Item.objects.filter(owner=user)
    citems = Cart.objects.filter(user=user)
    if not len(orders):
        orders = ""
    if not len(items):
        items = ""
    cart_items = []
    for cart_item in citems:
        cat = Category.objects.get(pk=cart_item.categoryid)
        item = cat.item_set.get(pk=cart_item.itemid)
        cart_items.append(item)

    context = {
            'usname': user.username, 
            'orders': orders,
            'items': items,
            'cart_items': cart_items
    }
    return context

class index(TemplateView):
    template_name = 'items/index.html'
    #context_object_name = 'latest_categories_list'

    def get_context_data(self):
        #print(super().__dir__())
        #print(super().response_class.__dir__())
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

def add_to_cart(r, categoryid, itemid):
    user = User.objects.get(username=r.session['usname'])
    c = Cart.objects.create(user=user, categoryid=categoryid, itemid=itemid, adding_date=timezone.now())
    c.save()

    return HttpResponseRedirect(f'/sklapp/{categoryid}')

def del_from_cart(r, position):
    user = User.objects.get(username=r.session['usname'])
    c = Cart.objects.filter(user=user)
    c = c.order_by('adding_date')
    for i, line in enumerate(c):
        if i+1 == position:
            line.delete()

    return HttpResponseRedirect('/sklapp/profile/')

def clear_the_cart(r):
    user = User.objects.get(username=r.session['usname'])
    c = Cart.objects.filter(user=user)
    c.delete()
    return HttpResponseRedirect('/sklapp/profile/')

class profile(base.View):
    def get(self, r, *args, **kwargs):
        if 'usname' in r.session.keys():
            context = get_cart_context(r.session["usname"])
            #print(context)
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
            context = get_cart_context(user.username)
            context['forms'] = form
            context['categories'] = Category.objects.all()
            return render(r, 'items/add_item.html', context)
    else:
        return HttpResponseRedirect('/sklapp/login/')

class login(base.View):
    def get(self, r, *args, **kwargs):
        if r.session['usname']:
            return HttpResponseRedirect('/sklapp/profile/')
        else:
            form = LoginForm()
            context = {"forms":form}
            return render(r, 'items/login.html', context)

    def post(self, r, *args, **kwargs):
        form = LoginForm()
        context = {"forms":form}
        if 'usname' in r.POST and 'passwd' in r.POST:
            usname, passwd = r.POST['usname'],r.POST['passwd']
            user = authenticate(username=usname, password=passwd)
            # correct password
            if user:
                r.session['usname'] = str(user)
                return HttpResponseRedirect('/sklapp/profile/')

            # wrong password
            else:
                context["error_message"] = "Wrong password"
        else:
            context["error_message"] = "Fill empty brackets"
        return render(r, 'items/login.html', context)

class register(base.View):
    def get(self, r, *args, **kwargs):
        form = CreateUserForm()
        context = {"forms": form}
        return render(r, 'items/register.html', context)
    def post(self, r, *args, **kwargs):
        form = CreateUserForm()
        context = {"forms": form}
        # create an user
        fields = ['usname','email','passwd1','passwd2']
        condition=[s in r.POST for s in fields]
        if min(condition):
            username, email, passwd1, passwd2 = [r.POST[s] for s in fields]
            if username in User.objects.all():
                context["error_message"] = "User exists"
            # creating an user
            elif passwd1 == passwd2:
                user = User.objects.create_user(username, email, passwd1)
                user.save()
                return HttpResponseRedirect('/sklapp/login/')
            else:
                context["error_message"] = "passwords aren't the same"
        return render(r, 'items/register.html', context)

"""
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
            user = User.objects.create_user(username, email, passwd1)
            user.save()
            return HttpResponseRedirect('/sklapp/login/')
        else:
            context["error_message"] = "passwords aren't the same"
    return render(r, 'items/register.html', context)

"""
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

def checkout(r):
    #category = get_object_or_404(Category, pk=category_id)
    user = User.objects.get(username=r.session['usname'])
    try:
        cart_items = Cart.objects.filter(user=user)
        print(cart_items)
    except (KeyError, Cart):
        return render(r, 'items/items.html', {
            'usname': r.session['usname'],
            'category': category,
            'error_message': "You picked nothing",
        })
    else:
        #u = User.objects.get(username=r.session['usname'])
        #for item in category.item_set.all():
        for cart_item in cart_items:
            c = Category.objects.get(id=cart_item.categoryid)
            item = c.item_set.get(id=cart_item.itemid)
            item.price += 0.01
            item.save()
            Order.objects.create(user=user, item_name=item, purchase_date=timezone.now())

        return HttpResponseRedirect(reverse('items:clear_the_cart'))


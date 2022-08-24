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

from collections import Counter

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
            'cart_items': Counter(cart_items).items()
    }
    return context

class index(TemplateView):
    template_name = 'items/index.html'

    """
    def get(self, r, **kwargs):
        return HttpResponseRedirect('/sklapp/login/')
    """

    def get_context_data(self, **kwargs):
        if "usname" in self.request.session.keys():
            user = self.request.session["usname"]
            context = get_cart_context(user)
            context['categories'] = Category.objects.all()
            return context


class items(TemplateView):
    template_name = 'items/items.html'

    def get_context_data(self, *args, **kwargs):
        user = self.request.session["usname"]
        context = get_cart_context(user)
        cid = kwargs['category_id']
        context['category'] = get_object_or_404(Category, pk=cid)
        print(context)
        return context

class results(TemplateView):
    template_name = 'items/results.html'

    def get_context_data(self, **kwargs):
        cid = self.kwargs['category_id']
        cat = get_object_or_404(Category, pk=cid)
        return {'category': cat}

class CartView:
    "cart methods"
    def add_to_cart(r, categoryid, itemid):
        if 'usname' in r.session:
            user = User.objects.get(username=r.session['usname'])
            c = Cart.objects.create(user=user, categoryid=categoryid, itemid=itemid, adding_date=timezone.now())
            c.save()
            print('sprawdz')
            return HttpResponseRedirect(f'/sklapp/{categoryid}/')
        else:
            return HttpResponseRedirect('/sklapp/login/')

    def del_from_cart(r, position):
        if 'usname' in r.session:
            user = User.objects.get(username=r.session['usname'])
            c = Cart.objects.filter(user=user)
            c = c.order_by('adding_date')
            for i, line in enumerate(c):
                if i+1 == position:
                    line.delete()
            
            current_site = r.path.split('/')[-1]
            return HttpResponseRedirect(f'/sklapp/{current_site}')
        else:
            return HttpResponseRedirect('/sklapp/login/')


    def clear_the_cart(r):
        user = User.objects.get(username=r.session['usname'])
        c = Cart.objects.filter(user=user)
        c.delete()
        return HttpResponseRedirect('/sklapp/profile/')


class profile(TemplateView):
    template_name = 'items/profile.html'

    def get(self, r, **kwargs):
        template_name = 'items/profile.html'
        user = self.request.session["usname"]
        if user:
            context = get_cart_context(user)
            return render(r, template_name, context)
        else:
            return HttpResponseRedirect('/sklapp/login/')

def add_item(r):
    if r.session['usname']:
        user = User.objects.get(username=r.session['usname'])
        if 'itemname' in r.POST and 'categoryid' in r.POST and 'price' in r.POST and 'count' in r.POST:
            category, itemname, price, count = r.POST['categoryid'], r.POST['itemname'], r.POST['price'], r.POST['count']
            c = Category.objects.get(id=category)
            c.item_set.create(owner=user.username, item_name=itemname,price=price, count=count)
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

class login(TemplateView):
    template_name = 'items/login.html'

    def post(self, r, *args, **kwargs):
        template_name = 'items/login.html'
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
        return render(r, template_name, context)


    def get(self, r, *args, **kwargs):
        template_name = 'items/login.html'
        if "usname" in r.session:
            user = self.request.session["usname"]
            return HttpResponseRedirect('/sklapp/profile/')
        else:
            form = LoginForm()
            context = {"forms":form}
            return render(r, template_name, context)

class register(TemplateView):
    template_name = 'items/register.html'

    def post(self, r, *args, **kwargs):
        form = CreateUserForm()
        context = {"forms": form}
        # create an user
        fields = ['usname','email','passwd1','passwd2']
        condition=[s in r.POST for s in fields]
        if min(condition):
            username, email, passwd1, passwd2 = [r.POST[s] for s in fields]
            username = username.lower()
            if username in User.objects.all():
                context["error_message"] = "User exists"
            # creating an user
            elif passwd1 == passwd2:
                user = User.objects.create_user(username, email, passwd1)
                user.save()
                return HttpResponseRedirect('/sklapp/login/')
            else:
                context["error_message"] = "passwords aren't the same"
        else:
            context["error_message"] = "fill empty brackets"
        return render(r, template_name, context)

    def get_context_data(self, *args, **kwargs):
        form = CreateUserForm()
        context = {"forms": form}
        return context

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
            context["error_message"]= "passwords are not the same"
    else:
        context["error_message"]= "Fill missing fields"
    return render(r, 'items/change_password.html', context)

def logout(r):
    try:
        del r.session['usname']
    except KeyError:
        pass
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
        u = User.objects.get(username=r.session['usname'])
        #for item in category.item_set.all():
        for cart_item in cart_items:
            c = Category.objects.get(id=cart_item.categoryid)
            item = c.item_set.get(id=cart_item.itemid)
            item.count -= 1
            item.save()
            number = Order.objects.count()
            Order.objects.create(user=user, item_name=item, purchase_date=timezone.now(), number=number)
        #Order.objects.create(user=user, items=str(dict(Counter(cart_items))), purchase_date=timezone.now())

        return HttpResponseRedirect(reverse('items:clear_the_cart'))


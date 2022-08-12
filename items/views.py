from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Category, Item, Order
from .forms import LoginForm, ChangePasswordForm, CreateUserForm

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

def profile(r):
    if 'usname' in r.session.keys():
        user = User.objects.get(username=r.session['usname'])
        orders = Order.objects.get(pk=user.id) if Order.objects.count() > 0 else "We haven't orders"
        context = {
                'usname': user.username, 
                'orders': orders
        }
        return render(r, 'items/profile.html', context)

def login(r):
    form = LoginForm()
    context = {"forms":form}
    #if 'usname' in r.POST and 'passwd' in r.POST:
    if len(r.POST) == 2:
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
    #if len(r.POST.keys()) == 4:
    if len(r.POST) == 4:
        username, email, passwd1, passwd2 = [r.POST[s] for s in ['usname','email','passwd1','passwd2']]
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
    form = ChangePasswordForm()
    context = {"forms": form}
    usname = r.session['usname']
    #if len(r.POST.keys()) == 2:
    if len(r.POST) == 2:
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
            'category': category,
            'error_message': "You picked nothing",
        })
    else:
        for item in category.item_set.all():
            if str(item.pk) in selected_items:
                item.price += 0.01
                item.save()
        return HttpResponseRedirect(reverse('items:results', args=(category_id,)))

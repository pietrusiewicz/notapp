from django.urls import path

from . import views

app_name = 'items'
urlpatterns = [
    #path('', views.IndexView.as_view()),
    path('', views.index.as_view(), name='index'),
    path('<int:category_id>/', views.items.as_view(), name='items'),
    path('<int:category_id>/results/', views.results.as_view(), name='results'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_to_cart/<int:categoryid>/<int:itemid>', views.add_to_cart, name='add_to_cart'),
    path('del_from_cart/<int:position>/', views.del_from_cart, name='del_from_cart'),
    path('clear_the_cart/', views.clear_the_cart, name='clear_the_cart'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_item/', views.add_item, name="add_item")
]

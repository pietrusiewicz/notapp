from django.urls import path

from . import views

app_name = 'items'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:category_id>/', views.items, name='items'),
    path('<int:category_id>/results/', views.results, name='results'),
    path('<int:category_id>/order/', views.order, name='order'),
]

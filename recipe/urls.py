from django.urls import path
from .views import (
    recipe_list,
    recipe_detail,
    my_recipe_list,
    recipe_create,
    recipe_update,
    recipe_delete,
    ingredient_create,
    ingredient_change,
    ingredient_delete,
)


app_name = "recipe"

urlpatterns = [
    path('list/', recipe_list, name='list'),
    path('list/my/', my_recipe_list, name='my-list'),
    path('list/<slug:slug>/', recipe_detail, name='detail'),
    path('create/', recipe_create, name='create-form'),
    path('update/<slug:slug>/', recipe_update, name='update'),
    path('delete/<slug:slug>/', recipe_delete, name='delete'),
    path('<slug:slug>/ingredient/create/', ingredient_create, name='ingredient-create-form'),
    path('<slug:slug>/ingredient/change/<int:pk>/', ingredient_change, name='ingredient-change-form'),
    path('<slug:slug>/ingredient/delete/<int:pk>/', ingredient_delete, name='ingredient-delete-form')

]
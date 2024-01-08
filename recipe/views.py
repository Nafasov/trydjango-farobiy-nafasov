from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator


from .models import Tag, Recipe, Ingredient
from .forms import RecipeForm, IngredientForm


def recipe_list(request):
    q = request.GET.get('q')
    tag = request.GET.get('tag')
    q_condition = Q()
    if q:
        q_condition = Q(title__icontains=q)
    tag_conditions = Q()
    if tag:
        tag_conditions = Q(tags__title=tag)
    recipes = Recipe.objects.filter(q_condition, tag_conditions).order_by("-id")
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "object_list": page_obj
    }
    return render(request, 'recipe/index.html', context)


def my_recipe_list(request):
    recipes = Recipe.objects.filter(author__id=request.user.id).order_by("-id")
    tag = request.GET.get('tag')
    if tag:
        recipes = recipes.filter(tags__title=tag)
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "object_list": page_obj
    }
    return render(request, 'recipe/index.html', context)


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    is_author_lookup = Q(is_active=True)
    if request.user == recipe.author:
        is_author_lookup = Q()
    ingredients = Ingredient.objects.filter(Q(recipe_id=recipe.id) & is_author_lookup)
    is_author = request.user == recipe.author
    context = {
        'object': recipe,
        'ingredients': ingredients,
        'is_author': is_author
    }
    return render(request, 'recipe/detail.html', context)


def recipe_create(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You should login in first!')
        reverse_url = reverse('auth:login') + '?next=' + request.path
        # print(request.path)
        return redirect(reverse_url)
    form = RecipeForm()
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author_id = request.user.id
            obj.save()
            form.save_m2m()
            reverse_url = reverse('recipe:detail', args=[obj.slug])
            return redirect(reverse_url)
    context = {
        'form': form,

    }
    return render(request, 'recipe/create.html', context)


def recipe_update(request, slug):
    instance = get_object_or_404(Recipe, slug=slug)
    form = RecipeForm(instance=instance)
    if request.method == "POST":
        if not request.user == instance.author:
            messages.warning(request, 'You have no enough permission to update!')
            return redirect(reverse('recipe:detail', args=[instance.slug]))
        form = RecipeForm(data=request.POST, files=request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            reverse_url = reverse('recipe:detail', kwargs={'slug': instance.slug})
            return redirect(reverse_url)
    context = {
        'form': form,
        'header': 'Recipe Update',
        'instance': instance
    }
    return render(request, 'recipe/create.html', context)


def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.method == "POST":
        if not request.user == recipe.author:
            messages.warning(request, 'You have no enough permission to delete!')
            return redirect(reverse('recipe:detail', args=[recipe.slug]))
        recipe.delete()
        return redirect('recipe:list')
    context = {
        'object': recipe
    }
    return render(request, 'recipe/delete.html', context)


def ingredient_create(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    reverse_url = reverse('recipe:detail', args=[recipe.slug])
    if request.user != recipe.author:
        messages.error(request, 'You have no enough permission')
        return redirect(reverse_url)
    form = IngredientForm()
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.recipe = recipe
            obj.save()
            messages.success(request, f'You created ingredient "{obj.title}".')
            return redirect(reverse_url)
    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'recipe/ingredient_create.html', context)


def ingredient_change(request, slug, pk, *args, **kwargs0):
    recipe = get_object_or_404(Recipe, slug=slug)
    reverse_url = reverse('recipe:detail',args=[recipe.slug])
    instance = get_object_or_404(Ingredient, id=pk)
    if instance not in recipe.ingredients.all():
        raise ObjectDoesNotExist(f"{instance.title} does not exist in {recipe.title}")
    if request.user != recipe.author:
        messages.error(request, 'You have no enough permission')
        return redirect(reverse_url)
    form = IngredientForm(instance=instance)
    if request.method == "POST":
        form = IngredientForm(data=request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'You changed an ingredient "{obj.title}.')
            return redirect(reverse_url)
    context = {
        'form': form,
        'recipe': recipe,
        'ingredient': instance,
    }
    return render(request, 'recipe/ingredient_change.html', context)


def ingredient_delete(request, *args, **kwargs):
    recipe = get_object_or_404(Recipe, slug=kwargs['slug'])
    instance = get_object_or_404(Ingredient, id=kwargs['pk'])
    reverse_url = reverse('recipe:detail', args=[recipe.slug])
    if instance not in recipe.ingredients.all():
        raise ObjectDoesNotExist(f"{instance.title} does not exist in {recipe.title}")
    if request.user != recipe.author:
        messages.error(request, 'You have no enough permission')
        return redirect(reverse_url)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, f'"{instance.title}" ingredient deleted successfully!')
        return redirect(reverse_url)
    context = {
        'recipe': recipe,
        'ingredient': instance,
    }
    return render(request, 'recipe/ingredient_delete.html', context)

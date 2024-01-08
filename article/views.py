from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.core.paginator import Paginator


from .models import Article
from .forms import ArticleForm


def article_list(request):
    query = request.GET.get('q')
    articles = Article.objects.search(query=query)
    paginator = Paginator(articles, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list': page_obj,
    }
    return render(request, 'article/index.html', context)


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    context = {
        'object': article
    }
    return render(request, 'article/detail.html', context)


def article_create(request):
    context = {
        'created': False
    }
    # print(request.method)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        obj = Article.objects.create(title=title, content=content)
        context['created'] = True
        context['object'] = obj
    return render(request, 'article/create.html', context)


def article_create_form(request):
    form = ArticleForm()
    if request.method == 'POST':
        # print(request.POST)
        form = ArticleForm(request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save()
            reverse_url = reverse('article:detail', kwargs={"slug": obj.slug})
            return redirect(reverse_url)
    context = {
        'form': form
    }
    return render(request, 'article/create_form.html', context)


def article_change(request, slug):
    obj = Article.objects.get(slug=slug)
    form = ArticleForm(instance=obj)
    if request.method == "POST":
        form = ArticleForm(data=request.POST, instance=obj, files=request.FILES)
        if form.is_valid():
            form.save()
            reverse_url = reverse('article:change-form', kwargs={"pk": obj.slug})
            return redirect(reverse_url)
    context = {
        'form': form,
        'object': obj,
    }
    return render(request, 'article/edit.html', context)


def article_delete(request, slug):
    obj = get_object_or_404(Article, slug=slug)
    print(request.method)
    if request.method == 'POST':
        obj.delete()
        return redirect('article:list')
    context = {
        'object': obj,
    }
    return render(request, 'article/delete.html', context)














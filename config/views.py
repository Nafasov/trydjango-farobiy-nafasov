import random
from django.shortcuts import HttpResponse
from article.models import Article



def hello(request):
    obj_id = random.randint(1, 2)
    article = Article.objects.get(id = obj_id)
    title = f"<h1>{article.title} ({article.id})</h1>"
    content = f"<h1>{article.content}</h1>"
    my_str = title + content
    return HttpResponse(my_str)


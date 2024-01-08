from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'modified_date', 'created_date')
    # fields = ('title','content', 'modified_date', 'created_date')
    readonly_fields = ('modified_date', 'created_date')
    list_filter = ('created_date', )
    date_hierarchy = 'created_date'
    list_display_links = ('id', 'title', )
    search_fields = ('title', )
    save_as_continue = True
    ordering = ('id', )
    list_per_page = 25
    prepopulated_fields = {"slug": ("title", )}


admin.site.register(Article, ArticleAdmin)




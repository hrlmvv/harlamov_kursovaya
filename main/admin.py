from django.contrib import admin
from .models import Category, Profile, News, Article


def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)

make_published.short_description = "Опубликовать выбранные записи"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    actions = [make_published]
    search_fields = ('title', 'author__username', 'author__first_name', 'author__last_name')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    actions = [make_published]
    search_fields = ('title', 'author__username', 'author__first_name', 'author__last_name')

admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(News, NewsAdmin)
admin.site.register(Article, ArticleAdmin)
from django.contrib import admin
from django_boost.admin import LogicalDeletionModelAdmin

from .models import Customer, Article, Tag, Category


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'registered_at')


@admin.register(Article)
class ArticleAdmin(LogicalDeletionModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


from django.contrib import admin
from .models import Author, Category, Entry


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'first_name', 'last_name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'category')

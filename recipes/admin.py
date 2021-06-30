from django.contrib import admin

from .models import Favorite, Follow, Ingredient, Recipe, RecipeIngredient, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('^name', )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('name', 'author', )
    list_filter = ('author', 'name', 'tags')
    prepopulated_fields = {'slug': ('name',)}


class FollowAdmin(admin.ModelAdmin):
    model = Follow


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('recipe', 'user', )
    list_filter = ('user', )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView)

from .models import Recipe, Tag
from .forms import RecipeForm

from .mixins import SectionMixin, TagMixin
from shopping_list.views import ShopListMixin

User = get_user_model()


class IndexView(ShopListMixin, SectionMixin, TagMixin, ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.GET.getlist("tags")
        all_tags = [tag.slug for tag in self.all_tags]
        tags = list(set(all_tags) - set(tags))
        return queryset.filter(tags__slug__in=tags).distinct()


class MyFollowView(ShopListMixin, SectionMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = 'recipe/myFollow.html'
    paginate_by = 6

    def get_queryset(self):
        authors = User.objects.filter(
            following__user=self.request.user).prefetch_related('recipes')
        return authors


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'recipe/singlePage.html'


class RecipeNew(ShopListMixin, SectionMixin, LoginRequiredMixin, CreateView):
    form_class = RecipeForm
    template_name = 'recipe/formRecipe.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdate(ShopListMixin, SectionMixin, LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/formRecipe.html'
    success_url = reverse_lazy('index')


class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipe/recipe_check_delete.html'
    success_url = reverse_lazy('index')


class AuthorView(ShopListMixin, SectionMixin, TagMixin, ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipe/authorRecipe.html'
    paginate_by = 6

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs.get('author'))
        tags = self.request.GET.getlist("tags")
        all_tags = [tag.slug for tag in self.all_tags]
        tags = list(set(all_tags) - set(tags))
        if tags:
            return author.recipes.all().filter(tags__slug__in=tags).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(
            User, username=self.kwargs.get('author'))
        return context


class FavoriteListView(ShopListMixin, SectionMixin, TagMixin, ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipe/favorite.html'
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        tags = self.request.GET.getlist("tags")
        all_tags = [tag.slug for tag in self.all_tags]
        tags = list(set(all_tags) - set(tags))
        return Recipe.objects.filter(favorite__user=user, tags__slug__in=tags)

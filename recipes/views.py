from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from shopping_list.views import ShopListMixin

from .forms import RecipeForm
from .mixins import SectionMixin, TagMixin
from .models import Recipe

User = get_user_model()


class IndexView(ShopListMixin, SectionMixin, TagMixin, ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.get_tags()
        return queryset.filter(tags__slug__in=tags).distinct()


class MyFollowView(LoginRequiredMixin, ShopListMixin, SectionMixin, ListView):
    model = User
    template_name = 'recipe/myFollow.html'
    paginate_by = 6

    def get_queryset(self):
        return User.objects.filter(
            following__user=self.request.user).prefetch_related('recipes')


class RecipeDetail(ShopListMixin, DetailView):
    model = Recipe
    template_name = 'recipe/singlePage.html'


class RecipeNew(LoginRequiredMixin, ShopListMixin, SectionMixin, CreateView):
    form_class = RecipeForm
    template_name = 'recipe/formRecipe.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdate(LoginRequiredMixin, ShopListMixin,
                   SectionMixin, UpdateView):
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
        tags = self.get_tags()
        return author.recipes.all().filter(tags__slug__in=tags).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(
            User, username=self.kwargs.get('author'))
        return context


class FavoriteListView(LoginRequiredMixin, ShopListMixin, SectionMixin,
                       TagMixin, ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipe/favorite.html'
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        tags = self.get_tags()
        return Recipe.objects.filter(favorite__user=user, tags__slug__in=tags)

import json
import weasyprint
from django.conf import settings

from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView

from recipes.models import Recipe, RecipeIngredient
from recipes.mixins import SectionMixin


class ShopList:
    """Список рецептов(покупок)."""
    def __init__(self, request) -> None:
        self.session = request.session
        shop_list = self.session.get('shop_list')
        if not shop_list:
            shop_list = self.session['shop_list'] = []
        self.shop_list = shop_list

    def save(self):
        self.session.modified = True

    def add(self, recipe_id: int):
        if recipe_id not in self.shop_list:
            self.shop_list.append(recipe_id)
            self.save()

    def remove(self, recipe_id: int):
        if recipe_id in self.shop_list:
            self.shop_list.remove(recipe_id)
            self.save()


class ShopListMixin:
    """Добавляет в context shop_list."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop_list = ShopList(self.request)
        purchases_count = len(shop_list.shop_list)
        context["shop_list"] = shop_list.shop_list
        context['purchases_count'] = purchases_count
        return context


class ShoppingListView(ShopListMixin, SectionMixin, ListView):
    model = Recipe
    template_name = 'shopping_list/shopList.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        shop_list = ShopList(self.request)
        queryset = Recipe.objects.filter(id__in=shop_list.shop_list)
        return queryset

    def post(self, request):
        req_ = json.loads(request.body)
        shop_list = ShopList(request)
        recipe_id = req_.get("id")
        if recipe_id is not None:
            shop_list.add(int(recipe_id))
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        shop_list = ShopList(request)
        shop_list.remove(int(recipe_id))
        return JsonResponse({"success": True})


def get_pdf(request):
    shop_list = ShopList(request)
    recipe_list = Recipe.objects.filter(id__in=shop_list.shop_list)
    ingredient_list = (
        RecipeIngredient.objects.filter(recipe__id__in=shop_list.shop_list)
        .values("ingredient__name", "ingredient__unit")
        .annotate(amountsum=Sum("amount"))
    )
    html_string = render_to_string('shopping_list/shopping_list_pdf.html',
                                   {'recipe_list': recipe_list,
                                    'ingredients': ingredient_list})
    response = HttpResponse(content_type='application/pdf; charset=utf-8')
    response['Content-Disposition'] = 'filename=list.pdf'

    weasyprint.HTML(string=html_string).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(str(settings.STATIC_ROOT) + '/shopping_list_pdf.css')
        ],
    )
    return response

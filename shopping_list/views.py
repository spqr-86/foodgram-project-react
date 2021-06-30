import weasyprint
from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from recipes.mixins import SectionMixin
from recipes.models import Recipe, RecipeIngredient

from .mixins import ShopList, ShopListMixin


class ShoppingListView(ShopListMixin, SectionMixin, ListView):
    model = Recipe
    template_name = 'shopping_list/shopList.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        shop_list = ShopList(self.request)
        queryset = Recipe.objects.filter(id__in=shop_list.shop_list)
        return queryset


def get_pdf(request):
    shop_list = ShopList(request)
    recipe_list = Recipe.objects.filter(id__in=shop_list.shop_list)
    ingredient_list = (
        RecipeIngredient.objects.filter(recipe__id__in=shop_list.shop_list)
        .values('ingredient__name', 'ingredient__unit')
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

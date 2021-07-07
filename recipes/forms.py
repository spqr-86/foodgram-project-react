from django import forms

from .models import Ingredient, Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(), to_field_name='name'
    )

    class Meta:
        model = Recipe
        fields = [
            'name',
            'image',
            'description',
            'tags',
            'cooking_time',
            'slug',
            'ingredients',
        ]

        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            ingredients = self.get_ingredients(data)
            for item in ingredients:
                data.update({'ingredients': item})
            self.amount = self.get_amount(data)

        super().__init__(data=data, *args, **kwargs)

    def save(self, commit=True):
        recipe_obj = super().save(commit=False)
        recipe_obj.save()

        ingredients_amount = self.amount
        recipe_obj.ingredients_amounts.all().delete()

        recipe_obj.ingredients_amounts.set(
            [
                RecipeIngredient(
                    recipe=recipe_obj,
                    ingredient=ingredient,
                    amount=float(ingredients_amount[ingredient.name]),
                ).full_clean()
                for ingredient in self.cleaned_data['ingredients']
            ],
            bulk=False,
        )
        self.save_m2m()
        return recipe_obj

    def get_ingredients(self, query_data):
        """Возвращает список с названием ингредиентов."""
        return [
            query_data[key]
            for key in query_data.keys()
            if key.startswith('nameIngredient')
        ]

    def get_amount(self, q_dict):
        """Возвращает словарь ингредиент:количество."""
        result = {}
        for key in q_dict.keys():
            if key.startswith('nameIngredient'):
                n = key.split('_')[1]
                result[q_dict['nameIngredient_' + n]] = q_dict[
                    'valueIngredient_' + n
                ]
        return result

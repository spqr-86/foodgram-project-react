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
        context['shop_list'] = shop_list.shop_list
        context['purchases_count'] = purchases_count
        return context

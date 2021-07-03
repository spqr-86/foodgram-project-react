from django import template

register = template.Library()


@register.filter
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})


@register.filter
def is_favorite(recipe_id, user):
    return user.favorite.filter(recipe=recipe_id).exists()


@register.filter
def has_follower(author_id, user):
    return user.follower.filter(author=author_id).exists()


@register.filter
def in_purchases(recipe_id, session):
    recipes: list = session.get("shop_list")
    return recipes and recipe_id in recipes

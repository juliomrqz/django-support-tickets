from django.contrib.auth import get_user_model

from model_mommy.recipe import Recipe

User = get_user_model()

# user
user = Recipe(
    User,
    is_active=True
)

from resources.auth import RegisterUser, LoginUser
from resources.category import CategoryListCreate, CategoryUpdateDelete, CategoryRecipesList
from resources.recipe import RecipeListCreate, RecipeListUpdate, RecipeUpdateDelete
from resources.user import ChangePassword, PersonalInfo

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (ChangePassword, "/<string:username>/change-password"),
    (PersonalInfo, "/<string:username>/personal_info"),
    (RecipeListCreate, "/<string:username>/recipes"),
    (RecipeUpdateDelete, "/<string:username>/recipes/<int:recipe_pk>"),
    (RecipeListUpdate, "/recipe/<int:recipe_pk>"),
    (CategoryListCreate, "/categories"),
    (CategoryUpdateDelete, "/category/<int:category_pk>"),
    (CategoryRecipesList, "/categories/<int:category_pk>/recipes")
)

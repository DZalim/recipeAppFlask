from resources.auth import RegisterUser, LoginUser
from resources.category import CategoryListCreate
from resources.recipe import RecipeListCreate, RecipeListUpdate, RecipeUpdateDelete
from resources.user import ChangePassword, PersonalInfo

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (RecipeListCreate, "/<string:username>/recipes"),
    (RecipeUpdateDelete, "/<string:username>/recipes/<int:recipe_pk>"),
    (ChangePassword, "/<string:username>/change-password"),
    (CategoryListCreate, "/categories"),
    (PersonalInfo, "/<string:username>/personal_info"),
    (RecipeListUpdate, "/recipe/<int:recipe_pk>"),


)

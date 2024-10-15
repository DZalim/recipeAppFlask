from resources.auth import RegisterUser, LoginUser, ChangePassword
from resources.category import CategoryListCreate
from resources.recipe import RecipeListCreate

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (RecipeListCreate, "/user/recipes"),
    (ChangePassword, "/<string:username>/change-password"),
    (CategoryListCreate, "/categories")

)

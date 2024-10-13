from resources.auth import RegisterUser, LoginUser
from resources.recipe import RecipeListCreate

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (RecipeListCreate, "/user/recipes"),

)


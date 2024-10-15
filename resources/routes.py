from resources.auth import RegisterUser, LoginUser
from resources.category import CategoryListCreate
from resources.recipe import RecipeListCreate
from resources.user import ChangePassword, PersonalInfo

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (RecipeListCreate, "/user/recipes"),
    (ChangePassword, "/<string:username>/change-password"),
    (CategoryListCreate, "/categories"),
    (PersonalInfo, "/<string:username>/personal_info"),

)

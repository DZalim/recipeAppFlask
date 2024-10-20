from resources.auth import RegisterUser, LoginUser
from resources.category import CategoryListCreate, CategoryUpdateDelete, CategoryRecipesList
from resources.comment import RecipeComments, RecipeCommentUpdateDelete
from resources.recipe import RecipeListCreate, RecipeListUpdate, RecipeUpdateDelete
from resources.user import ChangePassword, PersonalInfo, DeactivateProfile

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (PersonalInfo, "/<string:username>/personal_info"),
    (DeactivateProfile, "/<string:username>/deactivate_profile"),
    (ChangePassword, "/<string:username>/change-password"),
    (CategoryListCreate, "/categories"),
    (CategoryUpdateDelete, "/category/<int:category_pk>"),
    (RecipeListCreate, "/<string:username>/recipes"),
    (RecipeUpdateDelete, "/<string:username>/recipes/<int:recipe_pk>"),
    (RecipeListUpdate, "/recipe/<int:recipe_pk>"),
    (CategoryRecipesList, "/categories/<int:category_pk>/recipes"),
    (RecipeComments, "/recipe/<int:recipe_pk>/comment"),
    (RecipeCommentUpdateDelete, "/recipe/<int:recipe_pk>/comment/<int:comment_pk>")

)

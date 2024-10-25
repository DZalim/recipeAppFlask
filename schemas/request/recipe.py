from schemas.base.recipe import BaseRecipeSchema
from schemas.request.photo import PhotoRequestSchema


class CreateRecipeRequestSchema(BaseRecipeSchema, PhotoRequestSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context['request_type'] = 'create'


class UpdateRecipeRequestSchema(BaseRecipeSchema, PhotoRequestSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context['request_type'] = 'update'

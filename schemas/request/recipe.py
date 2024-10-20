from schemas.base import BaseRecipeSchema


class CreateRecipeRequestSchema(BaseRecipeSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context['request_type'] = 'create'


class UpdateRecipeRequestSchema(BaseRecipeSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context['request_type'] = 'update'

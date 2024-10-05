import enum


class UserRoles(enum.Enum):
    beginner = "beginner"
    advanced = "advanced"
    admin = "admin"


class RecipeDifficultyLevel(enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

import enum


class UserRoles(enum.Enum):
    beginner = "beginner"
    advanced = "advanced"
    admin = "admin"


class ProfileStatus(enum.Enum):
    active = "active"
    inactive = "inactive"


class RecipeDifficultyLevel(enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

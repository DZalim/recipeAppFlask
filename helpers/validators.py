from marshmallow import ValidationError
from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    uppercase=1,
    lowercase=1,
    numbers=1,
    special=1,
)


def validate_password(value):
    errors = policy.test(value)

    if errors:
        error_messages = [str(error) for error in errors]
        raise ValidationError(f"Not a valid password. "
                              f"The password must contain: {', '.join(error_messages)}")


def validate_spaces_factory(field_name):
    def validate_spaces(value):
        value_parts = value.split()

        if len(value_parts) != 1:
            raise ValidationError(f"{field_name.capitalize()} cannot contain spaces. Must be one word!")

    return validate_spaces

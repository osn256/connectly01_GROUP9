from django.core.exceptions import ValidationError

def validate_no_special_characters(value):
    if any(char in "!@#$%^&*()_+={}[]|\\:;\"'<>,.?/~`" for char in value):
        raise ValidationError('Value contains special characters, which are not allowed.')
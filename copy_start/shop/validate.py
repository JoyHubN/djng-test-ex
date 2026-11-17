from django.core.exceptions import ValidationError

def validate_file_size(value):
    # Ограничение в байтах. Например, 5 МБ = 5 * 1024 * 1024
    limit_mb = 5
    max_size = limit_mb * 1024 * 1024
    
    if value.size > max_size:
        raise ValidationError(f'Файл слишком большой. Максимальный размер: {limit_mb} МБ.')

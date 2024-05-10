import random

from users.models import Codes


def generate_code(user):
    code_str = ''.join(random.choices('0123456789', k=6))  # Генерация случайного 6-значного кода
    code = Codes.objects.filter(user=user).first()
    if not bool(code):
        code = Codes(user=user, code=code_str)
    else:
        code.code = code_str
    code.save()
    return code_str

from dateutil.utils import today
from rest_framework.exceptions import ValidationError
from datetime import  datetime, date

def validate_age_user(request):
    birthdate = request.auth.get('birthdate') if request.auth else None
    if not birthdate:
        raise ValidationError('Укажите дату рождения, чтобы создать продукт.')

    birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
    today = datetime.today().date()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if age < 18:
        raise ValidationError('Вам должно быть 18 лет, чтобы выполнить это дейсвие.')
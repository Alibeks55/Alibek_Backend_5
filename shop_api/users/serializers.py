from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import UsersCod, CustomUser

class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = serializers.CharField(required=False)


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserCreateSerializer(UserBaseSerializer):
    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError('CustomUser already exists!')


class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('User does not exist!')

        try:
            confirmation_code = UsersCod.objects.get(user=user)
        except UsersCod.DoesNotExist:
            raise ValidationError('Confirmation code not found!')

        if confirmation_code.code != code:
            raise ValidationError('Invalid confirmation code!')

        return attrs
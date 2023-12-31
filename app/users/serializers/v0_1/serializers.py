from rest_framework import serializers

from app.users.models import User
from app.users.utils import send_new_user_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "email",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super(UserSerializer, self).create(validated_data)

        if password:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            request_user = self.context["request"].user
            user.created_by = request_user
            user.save()

            send_new_user_email.delay(user.pk)

        return user

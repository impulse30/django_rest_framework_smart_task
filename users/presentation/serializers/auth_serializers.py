from rest_framework import serializers
from users.domain.entities.user import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        # Vérifier que les mots de passe correspondent
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Les mots de passe ne correspondent pas."})

        # Vérifier que l'email n'existe pas déjà
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Cet email est déjà utilisé."})

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

from rest_framework import serializers
from .models import Organization, User, Kudo

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'organization', 'remaining_kudos']

class KudoSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Kudo
        fields = ['id', 'from_user', 'to_user', 'message', 'created_at']

class GiveKudoSerializer(serializers.Serializer):
    to_user_id = serializers.UUIDField()
    message = serializers.CharField(max_length=500)
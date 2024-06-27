from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']


class VerifyCodeSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    class Meta:
        model = User
        fields = ["phone_number", "code"]


class ProfileActivatedInviteSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "avatar", "phone_number", "invite_code", "country", "city", "referred_users"]

    def get_referred_user(self, obj):
        referred_users = User.objects.filter(activated_invite_code=obj.invite_code)
        return [user.phone_number for user in referred_users]


class ProfileInputInviteSerializer(serializers.ModelSerializer):
    input_referral = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "avatar", "phone_number", "invite_code", "country", "city", "input_referral"]

    def update(self, instance, validated_data):
        input_referral = validated_data.pop("input_referral", None)
        if input_referral:
            referrer = User.objects.filter(invite_code=input_referral).first()
            if referrer:
                instance.activated_invite_code = input_referral
        return super().update(instance, validated_data)

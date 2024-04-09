from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework.pagination import PageNumberPagination

class UserRegistrationSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(required=False)  # Optional referral code field
    password_confirmation = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'password_confirmation', 'referral_code')
        extra_kwargs = {'password': {'write_only': True}}  

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)

        # Check if password and password_confirmation match
        if password != password_confirmation:
            raise serializers.ValidationError("Password and password confirmation do not match")

        # Validate password using Django's built-in password validators
        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e)

        return attrs

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        email = validated_data['email']

        # Check if referral_code exists in the User table
        referring_user = User.objects.filter(email=referral_code).first()
        if referring_user:
            # If referral code exists, store it
            user_referral_code = referral_code
            # Increment referral points for referring user
            referring_user.referral_points += 1
            referring_user.save()
        else:
            # If referral code doesn't exist, set it to None
            user_referral_code = None

        user = User.objects.create_user(
            email=email,
            name=validated_data['name'],
            password=validated_data['password'],
            referral_code=user_referral_code,  
        )

        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    referral_code = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('name', 'email','referral_code','date_joined')  
        
    def get_referral_code(self, obj):
        return obj.email

class ReferralSerializer(serializers.ModelSerializer):
    registration_timestamp = serializers.DateTimeField(source='date_joined')

    class Meta:
        model = User
        fields = ('name', 'email', 'registration_timestamp','referral_code')
        
class ReferralsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

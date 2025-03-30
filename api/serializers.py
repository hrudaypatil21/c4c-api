from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, UserProfile, NGOProfile

class IndividualRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    skills = serializers.CharField(required=True)
    interests = serializers.CharField(required=True)
    availability = serializers.CharField(required=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'confirm_password', 'first_name', 'last_name',
            'location', 'skills', 'interests', 'availability',
        ]
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match!")
        return data
    
    def create(self, validated_data):
        # Convert comma-separated strings to lists
        skills = [s.strip() for s in validated_data.pop('skills').split(',') if s.strip()]
        interests = [i.strip() for i in validated_data.pop('interests').split(',') if i.strip()]
        availability = validated_data.pop('availability')
        
        # Create user
        user = CustomUser.objects.create(
            user_type='individual',
            username=validated_data['email'],  # Will be regenerated in save()
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            location=validated_data.get('location', '')
        )
        
        
        # Create profile
        UserProfile.objects.create(
            user=user,
            skills=skills,
            interests=interests,
            availability=availability
        )
        
        return user

class NGORegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    vol_needs = serializers.CharField(required=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'confirm_password', 'org_name', 'reg_number',
            'org_phone', 'org_address', 'org_mission', 'org_website',
            'vol_needs', 'verification_docs',
        ]
        extra_kwargs = {
            'verification_docs': {'required': True},
            'org_name': {'required': True},
            'reg_number': {'required': True},
            'org_phone': {'required': True},
            'org_address': {'required': True},
            'org_mission': {'required': True},
        }
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match!")
        return data
    
    def create(self, validated_data):
        # Convert comma-separated strings to lists
        vol_needs = [v.strip() for v in validated_data.pop('vol_needs').split(',') if v.strip()]
        verification_docs = validated_data.pop('verification_docs')
        
        # Create user
        user = CustomUser.objects.create(
            user_type='ngo',
            username=validated_data['email'],  # Will be regenerated in save()
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            first_name=validated_data.get('org_name', '')  # Using org name as first name
        )
        
        # Create NGO profile
        NGOProfile.objects.create(
            user=user,
            org_name=validated_data['org_name'],
            reg_number=validated_data['reg_number'],
            org_phone=validated_data['org_phone'],
            org_address=validated_data['org_address'],
            org_mission=validated_data['org_mission'],
            org_website=validated_data.get('org_website', ''),
            vol_needs=vol_needs,
            verification_docs=verification_docs
        )
        
        return user
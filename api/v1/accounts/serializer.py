import datetime
import pandas as pd
from api.v1.accounts.utils import generate_emp_id, get_access_tokens_for_user, get_refres_tokens_for_user
from api.v1.models import *
from rest_framework import serializers
from django.conf import settings
import re
from django.db import transaction
from api.v1.models import UserMaster
from django.contrib.auth.hashers import make_password

class WebLoginSerializer(serializers.Serializer):
    email= serializers.CharField(max_length=100)
    password= serializers.CharField(max_length=100)
    remember_me= serializers.BooleanField(default=True)
    class Meta:
        model = UserMaster
        fields = ['email', 'password',"remember_me"]

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user_check = UserMaster.objects.filter(email=email,is_deleted=False).last()
        if not user_check:
            raise serializers.ValidationError({'error':'Entered email does not exists.'})
        
        if not user_check.is_active:
            raise serializers.ValidationError({'error':'Your Account is inactive.'})
        if not user_check.user_role_id in [1,2]:
            raise serializers.ValidationError({'error':'You are not allowed to login.'})
        
        if not (user_check.check_password(password)):
            raise serializers.ValidationError({'error':'You have entered wrong password.'})
        
        return attrs
    

class WebDetailsSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    user_role_id  = serializers.SerializerMethodField()
    
    class Meta:
        model = UserMaster
        fields = ['id','full_name','email','phone_number',"created_by",'username','user_role_id',
                    'user_role','is_active','access_token','refresh_token']
    def get_user_role_id(self,obj):
        return obj.user_role_id
    
    def get_user_role(self,obj):
        return obj.user_role.role
  
    def get_access_token(self, obj): 
        remember_me = self.context.get('remember_me')
        return get_access_tokens_for_user(obj.id,remember_me)

    def get_refresh_token(self, obj):
        remember_me = self.context.get('remember_me')
        return get_refres_tokens_for_user(obj.id,remember_me)

class DatasetSerializer(serializers.Serializer):
    file = serializers.FileField()
    class Meta:
        model = DatasetUpload
        fields =['file']

    def validate(self, attrs):
        file = attrs.get('file')
    
        mandatory_fields = {
            'file':file,
            }

        errors = {}

        for field, value in mandatory_fields.items():
            if not value:
                errors[field] = {'error': f'{field} is a mandatory field.'}

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user.id
        file = validated_data.get('file')
        if not UserMaster.objects.filter(id=user).exists():
            raise serializers.ValidationError({'error': "User doesn't exist."})

        with transaction.atomic():
            file_instance = DatasetUpload.objects.create(
                file=file,
                uploaded_by_id=user
            )
 
        return file_instance               
    

class UserRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(max_length=60, required=True)
    class Meta:
        model = UserMaster
        fields = ['name','email']

    def validate(self, attrs):
        email = attrs.get('email')

        if UserMaster.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({"error": "Email already exists."})
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            request=self.context.get('request')
            password = "Password@1"
            emp_id=generate_emp_id(2)
            user = UserMaster(
                full_name=validated_data['name'],
                email=validated_data['email'],
                username=validated_data['email'],
                password= make_password(password),
                raw_password=password,
                user_role_id=2,
                employee_id=emp_id,
                is_active=True,
                created_by_id=request.user.id,
            )
            user.save()
        return user    
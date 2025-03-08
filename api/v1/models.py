from django.db import models
from django.contrib.auth.models import  AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from api.v1.manager import CustomUserManager
from .manager import *

# Create your models here.
class Role(models.Model):
    Admin  = 1
    User  = 2
    
    ROLE_CHOICES = [
        (Admin , 'Admin '),
        (User , 'User ')
    
    ]
    role = models.CharField(max_length=25,default='Admin',null=False)
    created_on=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    class Meta:
        db_table = "user_roles"
    def __str__(self):
        return self.role
    

class UserMaster(AbstractBaseUser):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=50,null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    address = models.TextField(null=True)
    user_role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    employee_id=models.CharField(max_length=50,null=True,blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    raw_password = models.CharField(max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_logged_in=models.BooleanField(default=False)
    created_by = models.ForeignKey('UserMaster', on_delete=models.CASCADE, null=True, blank=True,related_name='user_created_by_id')
    created_on=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_on=models.DateTimeField(auto_now=True,blank=True,null=True)
    access_token = models.TextField(null=True)
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    class Meta:
        db_table = 'user_master'


class DatasetUpload(models.Model):
    file=models.FileField(upload_to='file_upload/',null=True)
    uploaded_by = models.ForeignKey('UserMaster', on_delete=models.CASCADE, null=True, blank=True,related_name='file_uploaded_by_id')
    created_on=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_on=models.DateTimeField(auto_now=True,blank=True,null=True)
    class Meta:
        db_table = 'dataset_upload'

        

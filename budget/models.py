from django.db import models
import re 
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors={}
        # NAME VALIDATOR
        if len(postData['first_name'])<1:
            errors['first_name'] = "First Name is Required"
        if len(postData['last_name'])<1:
            errors['last_name'] = "Last Name is Required"
        # EMAIL VALIDATIONS
        if len(postData['email'])< 1:
             errors['email'] = "Email is required."
        if not EMAIL_REGEX.match(postData['email']):  
            errors['email'] = "Invalid email address."
        existing_email = self.filter(email=postData['email'])
        if existing_email:
            errors['email'] = "Email already in use."
        # PASSWORD VALIDATOR
        if len(postData['password'])< 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm'] = "Passwords do not match."
        return errors

    def register(self, postData):
        hashed_password = bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hashed_password
        )
    
    def authenticate(self, email, password):
        users_with_email = self.filter(email=email)
        if not users_with_email:
            return False
        logged_user = users_with_email[0]
        return bcrypt.checkpw(password.encode(), logged_user.password.encode())

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Expense(models.Model):
    paid_to = models.CharField(max_length=255)
    amount = models.IntegerField()
    payer = models.ForeignKey("User", related_name=("bill_payer"), on_delete=models.CASCADE)
    due_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class Income(models.Model):
    amount = models.IntegerField()
    deposit_date = models.DateField()
    user = models.ForeignKey("User", related_name=("earner"), on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


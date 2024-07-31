from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from .QUESTION_TYPE import question_type, boolean_question
from django.conf import settings
User = settings.AUTH_USER_MODEL
from datetime import timezone

#from django.contrib.postgres.fields import ArrayField, JSONField

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user




class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    first_name = models.CharField(max_length=250, default='')
    last_name = models.CharField(max_length=250, default='')
    email_address = models.CharField(max_length=250, default='')
    mobile_number = models.CharField(max_length=250, default='')
    display_picture = models.ImageField(upload_to='Display Picture', default='')


    def __str__(self):
        return f'Profile :  {self.user}'




class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    survey_title = models.ForeignKey(
        'Poll', on_delete=models.SET_NULL, null=True, blank=True)
    choices = models.ForeignKey(
        'Choice', on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.survey_title}'

class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    survey_title = models.ForeignKey(
        'Poll', on_delete=models.SET_NULL, null=True, blank=True)
    #options = models.ForeignKey(
    #    'Options', on_delete=models.SET_NULL, null=True, blank=True)
    first_choice = models.CharField(max_length=100, blank=True)
    second_choice = models.CharField(max_length=100, blank=True)
    third_choice = models.CharField(max_length=100, blank=True)
    fourth_choice = models.CharField(max_length=100, blank=True)
    yes_or_no_choice = models.CharField(max_length=100, blank=True, choices=boolean_question, default='Choose Answer')
    #custom_choice = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
      


    def __str__(self):
        return  f'{self.survey_title} - {self.first_choice}'

class Options(models.Model):
    first_choice = models.CharField(max_length=100, blank=True)
    second_choice = models.CharField(max_length=100, blank=True)
    third_choice = models.CharField(max_length=100, blank=True)
    fourth_choice = models.CharField(max_length=100, blank=True)
    yes_or_no_choice = models.CharField(max_length=100, blank=True, choices=boolean_question, default='Choose Answer')
    #custom_choice = ArrayField(models.CharField(max_length=250, null=True, blank=True), default=list)  
      


    def __str__(self):
        return self.first_choice

# Create your models here.
class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    survey_title = models.CharField(max_length=100)
    choices = models.ManyToManyField(
        Choice, related_name='related_polls', blank=True)

    survey_type = models.CharField(max_length=100, blank=True, choices=question_type)
    slug = models.SlugField()
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.survey_title}')
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return self.survey_title






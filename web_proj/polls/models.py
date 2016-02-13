from __future__ import unicode_literals
import datetime
from django.utils.translation import ugettext as _
from django.db import models

# Create your models here.
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

	#extra info
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    info = models.TextField()
    age = models.IntegerField(default=0)
    gender = models.BooleanField(default=False)
    hobbies = models.TextField()
    height = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    birthday = models.DateField(default=timezone.now)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
	#override user's method
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email]) 


	# list of date request
    def add_relationship(self, person):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            )
        return relationship

    def remove_relationship(self, person):
        Relationship.objects.filter(
            from_person=self,
        to_person=person,
        ).delete()
        return
    def get_relationships(self):
        return self.relationships.filter(
            to_people__from_person=self)

    def get_related_to(self):
        return self.related_to.filter(
            from_people__to_person=self)

    def get_following(self):
        return self.get_relationships()

    def get_followers(self):
        return self.get_related_to()

	def get_all_followed(self):

		return Relationships.objects.filter(from_person=self)


    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.first_name



class Relationships(models.Model):
    from_person = models.ForeignKey(MyUser, related_name='from_people')
    to_person = models.ForeignKey(MyUser, related_name='to_people')

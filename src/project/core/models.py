from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from model_utils import fields


class UserManager(BaseUserManager):
    def create_user(self, email, screen_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            msg = _('Users must have an email address')
            raise ValueError(msg)
        if not screen_name:
            msg = _('User must have a screen name')
            raise ValueError(msg)

        user = self.model(
            email=UserManager.normalize_email(email),
            screen_name=screen_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, screen_name, password):
        """
        Create and saves a superuser with a given email and password.
        """
        user = self.create_user(email, screen_name=screen_name,
            password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Inherits from both the AbstractBaseUser and PermissionsMixin
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True
    )
    screen_name = models.CharField(max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['screen_name', ]

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created = fields.AutoCreatedField(_('created'))
    modified = fields.AutoLastModifiedField(_('modified'))

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their screen name and email
        return "%s <%s>" % (self.screen_name,
            self.email)

    def get_short_name(self):
        # The user is identified by their screen name
        return self.screen_name

    def __unicode__(self):
        return self.email

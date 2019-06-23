from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):

        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

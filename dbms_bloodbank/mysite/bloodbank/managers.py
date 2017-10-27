from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
	if not email:
	    raise ValueError('Email must be set.')

	user=self.model(email=self.normalize_email(email),is_active=True,is_staff=False,**kwargs)
	user.set_password(password)
	user.save(using=self._db)

	return user

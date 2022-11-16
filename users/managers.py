from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self, username, email, role, password=None, **extra_fields):

        if username is None:
            raise TypeError('You should provide a username')
        if email is None:
            raise TypeError('You should provide a email')
        if role is None:
            raise TypeError('You should provide a role')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            role=role
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, role, password, **extra_fields):
        print("create super user working...")
        if username is None:
            raise TypeError('You should provide a username')
        if email is None:
            raise TypeError('You should provide a email')
        if password is None:
            raise TypeError('You should provide a password')
        
        user = self.create_user(
            username=username,
            email=email,
            role='ADMIN'
        )

        user.is_verified = True
        user.is_superuser = True
        user.is_staff = True

        user.save()

        return user



from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """ Extend the BaseUserManager and pull the basic features from it 
    and overwrite a couple of functions to handle our email instead of username
    """
    def create_user(self, *arg, **kwargs):
        name = kwargs.get('name', None)
        email = kwargs.get('email', None)
        phone_number = kwargs.get('phone_number', None)
        password = kwargs.get('password', None)

        if not email:
            raise ValueError('Enter a valid e-mail address')

        user = self.model(
            name = name,
            phone_number = phone_number,
            email = self.normalize_email(email)
        )
        if password:
            user.set_password(password)
        
        user.save()

        return user
    
    def create_superuser(self, *args, **kwargs):
        '''Creates and saves new superuser'''

        name = kwargs.get('name', None)
        email = kwargs.get('email', None)
        phone_number = kwargs.get('phone_number', None)
        
        if not name:
            kwargs['name'] = 'Admin'
        
        if not email:
            kwargs['email'] = 'test@mail.com'

        if not phone_number:
            kwargs['phone_number'] = '8008008000'

        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

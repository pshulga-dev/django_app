from django.db import models
from django.contrib.auth.models import User, UserManager


class CustomUser(User):
    # timezone = models.CharField(max_length=50)

    objects = UserManager()

    class Meta:
        permissions = (
            ("admin", "Administrator"),
            ("user_short", "User Short"),
            ("user_admin", "User Administrator")
        )


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=130)
    address = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    website = models.CharField(max_length=520)
    user = models.ForeignKey('auth.User')
    company_logo = models.ImageField(blank=True, upload_to='/static/images/')

    class Meta:
        db_table = 'client'


class UserBD(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    password = models.CharField(max_length=520)

    class Meta:
        db_table = "user_db"


class Product(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "product"


def update_settings():
    from django.conf import settings
    DATABASES = settings.DATABASES
    try:

        db = UserBD.objects.all()
        if db.exists():
            for user in db:
                DATABASES.update({user.username: {"NAME": user.title,
                                                  "PASSWORD": user.password,
                                                  "USER": user.username,
                                                  'ENGINE': 'django.db.backends.postgresql',
                                                  'HOST': '127.0.0.1',
                                                  'PORT': '5432',}
                                  })
    except Exception as e:
        print(e)


update_settings()
